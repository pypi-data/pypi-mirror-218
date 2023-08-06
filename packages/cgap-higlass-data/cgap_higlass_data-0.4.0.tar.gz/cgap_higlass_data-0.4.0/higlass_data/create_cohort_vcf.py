import click
import vcf
import pandas as pd
import copy, os
import os.path
import negspy.coordinates as nc
from higlass_data.utils import does_tool_exist, get_chroms, get_vcf_header

TILE_SIZE = 1024  # Higlass tile size for 1D tracks
MAX_ZOOM_LEVEL = 23
CONSEQUENCE_LEVELS = ["HIGH", "LOW", "MODERATE", "MODIFIER"]


class MultiResVcf:

    
    def __init__(
        self,
        input_filepath,
        output_filepath,
        importance_column,
        max_variants_per_tile,
        chrom,
        quiet,
    ):
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.max_variants_per_tile = max_variants_per_tile
        self.importance_column = importance_column
        self.quiet = quiet
        self.variants = self.load_variants(chrom)
        self.variants_multires = []
        self.variants_df = []
        self.variants_by_id = {}
        self.chromosomes = self.get_chromosomes()
        self.tile_sizes = [TILE_SIZE * (2**i) for i in range(0, MAX_ZOOM_LEVEL)]
        self.chrom_info = nc.get_chrominfo("hg38")

    def create_multires_vcf(self):
        if len(self.variants) == 0:
            return
        self.assign_ids()
        self.index_variants_by_id()
        self.create_variants_dataframe()
        self.split_variants()
        self.aggregate()
        self.write_vcf()

    def aggregate(self):

        if not self.quiet:
            print("Start aggregation")

        for zoom_level, tile_size in enumerate(self.tile_sizes):
            if not self.quiet:
                print("  Current zoom level: ", zoom_level, ". Tile size: ", tile_size)

            # Don't do any aggregation, just copy the values with modified chr
            if zoom_level == 0:
                for id in self.variants_by_id:
                    variant = self.variants_by_id[id]  # Retrieve original data
                    variant_copy = copy.copy(variant)
                    if variant_copy.CHROM in self.chromosomes:
                        variant_copy.CHROM = variant_copy.CHROM + "_" + str(zoom_level)
                        self.variants_multires.append(variant_copy)
                continue

            current_index = 0

            num_tiles = 2 ** (MAX_ZOOM_LEVEL - zoom_level - 1)
            for current_index in range(0, num_tiles):

                variant_in_bin_ids = []
                variants_in_bin = self.variants_df_hierarchical[
                    str(zoom_level) + "." + str(current_index)
                ]

                current_index = current_index + 1
                new_pos = tile_size * current_index
                num_variants_in_bin = len(variants_in_bin.index)

                if num_variants_in_bin == 0:
                    continue

                if num_variants_in_bin < self.max_variants_per_tile:
                    variant_in_bin_ids += list(variants_in_bin.iloc[:, 1])
                else:
                    for consequence in CONSEQUENCE_LEVELS:
                        variants_per_consequence = variants_in_bin[
                            (variants_in_bin.consequence == consequence)
                        ]
                        num_variants_per_consequence = len(
                            variants_per_consequence.index
                        )

                        if num_variants_per_consequence > self.max_variants_per_tile:
                            if not self.quiet:
                                print(
                                    f"    Removing {num_variants_per_consequence - self.max_variants_per_tile} {consequence} variants from bin {tile_size * (current_index - 1)} - {new_pos} ({num_variants_in_bin} total variants)"
                                )
                            variants_per_consequence = (
                                variants_per_consequence.sort_values(
                                    by=["importance"], ascending=[False]
                                )[: self.max_variants_per_tile]
                            )

                        variant_in_bin_ids += list(variants_per_consequence.iloc[:, 1])

                variant_in_bin_ids.sort()
                for id in variant_in_bin_ids:
                    variant = self.variants_by_id[id]  # Retrieve original data
                    variant_copy = copy.copy(variant)
                    if variant_copy.CHROM in self.chromosomes:
                        variant_copy.CHROM = variant_copy.CHROM + "_" + str(zoom_level)
                        self.variants_multires.append(variant_copy)

    def split_variants(self):
        hierarchical_variant_data = {str(MAX_ZOOM_LEVEL - 1) + ".0": self.variants_df}

        for zoom_level in range((MAX_ZOOM_LEVEL - 1), 1, -1):

            num_tiles = 2 ** (MAX_ZOOM_LEVEL - zoom_level - 1)
            new_zoom_level = zoom_level - 1
            new_tile_size = TILE_SIZE * (2**new_zoom_level)
            for i_tile in range(0, num_tiles):
                tile_data = hierarchical_variant_data[f"{zoom_level}.{i_tile}"]
                if len(tile_data.index) > 0:
                    # Efficiently split the data using a boolean select
                    is_variant_in_left_half = tile_data["absPos"] < new_tile_size * (
                        2 * i_tile + 1
                    )
                    tile_data_split_left = tile_data[is_variant_in_left_half]
                    tile_data_split_right = tile_data[~is_variant_in_left_half]
                    hierarchical_variant_data[
                        f"{new_zoom_level}.{2*i_tile}"
                    ] = tile_data_split_left
                    hierarchical_variant_data[
                        f"{new_zoom_level}.{2*i_tile+1}"
                    ] = tile_data_split_right
                else:
                    # tile_data is just an empty DataFrame
                    hierarchical_variant_data[
                        f"{new_zoom_level}.{2*i_tile}"
                    ] = tile_data
                    hierarchical_variant_data[
                        f"{new_zoom_level}.{2*i_tile+1}"
                    ] = tile_data

        self.variants_df_hierarchical = hierarchical_variant_data

    def load_variants(self, chrom):
        if not self.quiet:
            print("Loading variants...")
        variants = []
        vcf_reader = vcf.Reader(filename=self.input_filepath)

        for record in vcf_reader:
            if not chrom:
                variants.append(record)
            elif chrom and record.CHROM == chrom:
                variants.append(record)

        if not self.quiet:
            print(f"Loading variants complete. Loaded {len(variants)} variants")
        return variants

    def index_variants_by_id(self):
        for variant in self.variants:
            self.variants_by_id[variant.ID] = variant

    def importance(self, importance_value):
        # We are treating each consequence level separately, therefore we are just returning the chosen importance value here
        # We could do something more fance here and make it dependent on the consequence level
        return importance_value

    # Create a matrix of the data that we use for filtering
    def create_variants_dataframe(self):
        chromosomes = []
        ids = []
        pos = []
        absPos = []
        importance = []
        consequence = []

        if not self.quiet:
            print("Creating data frame for easy querying during aggregation.")

        for variant in self.variants:

            chromosomes.append(variant.CHROM)
            ids.append(variant.ID)
            pos.append(variant.POS)
            absPos.append(
                nc.chr_pos_to_genome_pos(variant.CHROM, variant.POS, self.chrom_info)
            )
            importance_value = variant.INFO[self.importance_column][0]
            if importance_value == None or importance_value == "NA":
                importance_value = 0.0
            importance_value = float(importance_value)
            conseq = variant.INFO["level_most_severe_consequence"][0]

            if conseq not in CONSEQUENCE_LEVELS:
                print(f"Warning: Consequence level {conseq} not expected.")
            consequence.append(conseq)

            importance.append(self.importance(importance_value))

        d = {
            "chr": chromosomes,
            "id": ids,
            "pos": pos,
            "absPos": absPos,
            "consequence": consequence,
            "importance": importance,
        }
        self.variants_df = pd.DataFrame(data=d)

    def write_vcf(self):
        vcf_reader = vcf.Reader(filename=self.input_filepath)

        with open("tmp.output.vcf", "w") as output:
            vcf_writer = vcf.Writer(output, vcf_reader)
            for variant in self.variants_multires:
                vcf_writer.write_record(variant)
                vcf_writer.flush()
        


    def get_chromosomes(self):
        if not self.quiet:
            print("Extracting chromosomes...")
        chrs = list(set(map(lambda v: v.CHROM, self.variants)))
        if "chrM" in chrs:
            chrs.remove("chrM")
        chrs.sort()
        if not self.quiet:
            print("Chromosomes used: ", chrs)
        return chrs

    def assign_ids(self):
        id = 0
        for variant in self.variants:
            variant.ID = id
            id = id + 1

    
    # Currently unused. The idea was to not repeat variants on low zoom levels, if there is o aggregation.
    # This would have needed to be handled by the Higlass Cohort track accordingly. It's too complicated
    # and not worth it for now.
    def get_min_zoom_level(self):

        print("Calculating minimal zoom level")

        for zoom_level, tile_size in enumerate(self.tile_sizes):
            print("Checking zoom level", zoom_level, "with tile size", tile_size)
            current_pos = 0
            current_index = 0
            total_variants = 0

            for chr in self.chromosomes:
                chr_variants = self.variants_df[self.variants_df.chr == chr]
                last_pos = chr_variants["pos"].iloc[-1]
                while current_pos < last_pos:
                    new_index = current_index + 1
                    new_pos = tile_size * new_index
                    variants_in_bin = chr_variants[
                        (chr_variants.pos >= current_pos) & (chr_variants.pos < new_pos)
                    ]
                    num_variants_in_bin = len(variants_in_bin.index)
                    total_variants = total_variants + num_variants_in_bin
                    # if current_index % 1 == 0:
                    #     print(tile_size, current_pos, new_pos, num_variants_in_bin, total_variants)

                    if num_variants_in_bin > self.max_variants_per_tile:
                        print(
                            "Minimal zoom level found. Bin",
                            current_pos,
                            "-",
                            new_pos,
                            "has",
                            num_variants_in_bin,
                            "variants",
                        )
                        print(variants_in_bin)
                        self.min_zoom_level = max(0, zoom_level - 1)
                        return

                    current_index = new_index
                    current_pos = new_pos
                print("-- chromosome", chr, "done")



@click.command()
@click.help_option("--help", "-h")
@click.option("-i", "--input-vcf", required=True, type=str)
@click.option("-o", "--output-vcf", required=True, type=str)
@click.option(
    "-c",
    "--importance-column",
    required=True,
    type=str,
    help="Value in the info field of the VCF that should be sorted by",
)
@click.option(
    "-m", "--max-tile-values-per-consequence", default=50, required=False, type=int
)
@click.option(
    "-w", "--chromosome-wise", default=False, required=False, type=bool
)
@click.option("-t", "--index-output", required=False, default=True, type=bool)
@click.option("-q", "--quiet", required=False, default=True, type=bool)
def create_cohort_vcf(
    input_vcf, output_vcf, importance_column, max_tile_values_per_consequence, chromosome_wise, index_output, quiet
):
    input_filepath = input_vcf
    output_vcf_filepath = output_vcf
    max_variants_per_tile = max_tile_values_per_consequence

    if not does_tool_exist("bgzip"):
        raise Exception("bgzip is not installed.")
    if not does_tool_exist("tabix"):
        raise Exception("tabix is not installed.")

    if chromosome_wise:
        vcf_header = get_vcf_header()
        cmd = f"echo '{vcf_header}' > vcf_header.vcf"
        os.system(cmd)
        cmd = f"cat vcf_header.vcf | gzip > hgdata.tmp.header.vcf.gz"
        os.system(cmd)

        for chrom in get_chroms():
            mrv = MultiResVcf(
                input_filepath,
                f"hgdata.tmp.{chrom}.{output_vcf_filepath}",
                importance_column,
                max_variants_per_tile,
                chrom,
                quiet,
            )
            if output_vcf_filepath:
                mrv.create_multires_vcf()
                if os.path.exists("tmp.output.vcf"):
                    tmp_filename = f"hgdata.tmp.{chrom}.{output_vcf_filepath}"
                    cmd = f"cat tmp.output.vcf | tail -n +3 | gzip > {tmp_filename} || exit 1"
                    cmd_result = os.system(cmd)
                    if cmd_result > 0:
                        raise Exception(f"{cmd} failed.")
                    os.system(f"rm -f tmp.output.vcf")

        os.system(f"cat hgdata.tmp.header.vcf.gz hgdata.tmp* > multires.tmp.gz || exit 1") 
        os.system(f"rm -f hgdata.tmp*") 

        #Recompress with bgzip
        cmd_result = os.system(f"gzip -cd multires.tmp.gz | bgzip --threads 6 -c > {output_vcf_filepath} || exit 1")
        if cmd_result > 0:
            raise Exception(f"Recompression failed.")
        os.system(f"rm -f multires.tmp.gz")


    else:
        mrv = MultiResVcf(
            input_filepath,
            output_vcf_filepath,
            importance_column,
            max_variants_per_tile,
            None,
            quiet,
        )
        if output_vcf_filepath:
            mrv.create_multires_vcf()
            cmd_result = os.system(f"cat tmp.output.vcf | bgzip --threads 6 -c > {output_vcf_filepath} || exit 1")
            if cmd_result > 0:
                raise Exception(f"Compression failed.")

    if index_output:
        cmd = f"tabix -p vcf {output_vcf_filepath} || exit 1"
        cmd_result = os.system(cmd)
        if cmd_result > 0:
            raise Exception(f"{cmd} failed.")


if __name__ == "__main__":
    """
    Example:
    python create_cohort_vcf.py -i joint_calling_results.vcf -o joint_calling_results.multires.vcf -c regenie_log10p -q False
    """
    create_cohort_vcf()
