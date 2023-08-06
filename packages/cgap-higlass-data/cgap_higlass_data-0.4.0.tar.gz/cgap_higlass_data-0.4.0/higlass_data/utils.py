
def does_tool_exist(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which

    return which(name) is not None

def get_chroms():
    return ['chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX','chrY']

def get_vcf_header():
    return "##fileformat=VCFv4.3\n#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO"