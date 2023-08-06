import argparse
import csv
import inspect
import logging
import os
from datetime import datetime

from . import atlas, atlas_seurat, checkatlas_workflow, folders, multiqc

# try:
#     from . import atlas, folders, multiqc
# except ImportError:
#     import atlas
#     import folders
#     import multiqc


"""
checkatlas base module.
This is the principal module of the checkatlas project.

"""

EXTENSIONS = [".rds", ".h5ad", ".h5"]
CELLRANGER_FILE = "/outs/filtered_feature_bc_matrix.h5"
RSCRIPT = inspect.getfile(atlas).replace("atlas.py", "convertSeurat.R")
SUMMARY_EXTENSION = "_checkatlas_summ.tsv"
ADATA_EXTENSION = "_checkatlas_adata.tsv"
QC_FIG_EXTENSION = "_checkatlas_qc.png"
QC_EXTENSION = "_checkatlas_qc.tsv"
UMAP_EXTENSION = "_checkatlas_umap.png"
TSNE_EXTENSION = "_checkatlas_tsne.png"
METRIC_CLUSTER_EXTENSION = "_checkatlas_mcluster.tsv"
METRIC_ANNOTATION_EXTENSION = "_checkatlas_mannot.tsv"
METRIC_DIMRED_EXTENSION = "_checkatlas_mdimred.tsv"
METRIC_SPECIFICITY_EXTENSION = "_checkatlas_mspecificity.tsv"

logger = logging.getLogger("checkatlas")


def list_atlases(path: str) -> list:
    """
    List all atlases files in the path
    Detect .rds, .h5, .h5ad

    Args:
        path: Path for searching single-cell atlases.

    Returns:
        list: List of file atlases to check.
    """
    atlas_list = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            for extension in EXTENSIONS:
                if file.endswith(extension):
                    atlas_list.append(os.path.join(root, file))
    return atlas_list


def get_atlas_name(atlas_path: str) -> str:
    """
    From atlas_path extract the atlas_name
    Args:
        atlas_path:
    Returns:
        str: The atlas_name
    """
    return os.path.splitext(os.path.basename(atlas_path))[0]


def get_atlas_extension(atlas_path: str) -> str:
    """
    From atlas_path extract the atlas file extension
    Args:
        atlas_path:
    Returns:
        None
    """
    return os.path.splitext(os.path.basename(atlas_path))[1]


def clean_list_atlases(atlas_list: list, checkatlas_path: str) -> tuple:
    """
    Go through all files and detect Seurat, CellRanger or Scanpy Atlas
    The "cleaning means that we test if the atlas is valid or not.
    Args:
        atlas_list: list of atlases found with proper extension
        checkatlas_path: the path where checkatlas files are saved
    Returns:
         tuple: clean_atlas_scanpy, clean_atlas_seurat, clean_atlas_cellranger
    """
    clean_atlas_scanpy = dict()
    clean_atlas_seurat = dict()
    clean_atlas_cellranger = dict()
    for atlas_path in atlas_list:
        atlas_name = get_atlas_name(atlas_path)
        if atlas_path.endswith(".rds"):
            logger.debug(f"Include Atlas: {atlas_name} from {atlas_path}")
            info = [
                atlas_name,
                "Seurat",
                ".rds",
                os.path.dirname(atlas_path) + "/",
            ]
            clean_atlas_seurat[atlas_path] = info
        elif atlas_path.endswith(".h5"):
            # detect if its a cellranger output
            if atlas_path.endswith(CELLRANGER_FILE):
                atlas_h5 = atlas_path.replace(CELLRANGER_FILE, "")
                atlas_name = get_atlas_name(atlas_h5)
                logger.debug(f"Include Atlas: {atlas_name} from {atlas_path}")
                info = [
                    atlas_name,
                    "Cellranger",
                    ".h5",
                    os.path.dirname(atlas_h5) + "/",
                ]
                clean_atlas_cellranger[atlas_path] = info
        elif atlas_path.endswith(".h5ad"):
            logger.debug(f"Include Atlas: {atlas_name} from {atlas_path}")
            info = [
                atlas_name,
                "Scanpy",
                ".h5ad",
                os.path.dirname(atlas_path) + "/",
            ]
            clean_atlas_scanpy[atlas_path] = info
    # Save the list of atlas taken into account
    dict_file = open(
        os.path.join(
            folders.get_workingdir(checkatlas_path), "list_atlases.csv"
        ),
        "w",
    )
    w = csv.writer(dict_file)
    # loop over dictionary keys and values
    for key, val in clean_atlas_scanpy.items():
        w.writerow([key, ",".join(val)])
    for key, val in clean_atlas_seurat.items():
        w.writerow([key, ",".join(val)])
    for key, val in clean_atlas_cellranger.items():
        w.writerow([key, ",".join(val)])
    dict_file.close()
    return clean_atlas_scanpy, clean_atlas_seurat, clean_atlas_cellranger


def get_pipeline_functions(module, args) -> list:
    """
    Using arguments of checkatlas program -> build
    the list of functions to run on each adata
    and seurat object
    Args:
        module: Module to use either atlas or atlas_seurat
        args: List of args for checkatlas program
    Returns:
         list: list of functions to run
    """
    checkatlas_functions = list()

    if not args.NOADATA:
        checkatlas_functions.append(module.create_anndata_table)
    if not args.NOQC:
        if "violin_plot" in args.qc_display:
            checkatlas_functions.append(module.create_qc_plots)
        if (
            "total-counts" in args.qc_display
            or "n_genes_by_counts" in args.qc_display
            or "pct_counts_mt" in args.qc_display
        ):
            checkatlas_functions.append(module.create_qc_tables)
    if not args.NOREDUCTION:
        checkatlas_functions.append(module.create_umap_fig)
        checkatlas_functions.append(module.create_tsne_fig)
    if not args.NOMETRIC:
        if len(args.metric_cluster) > 0:
            checkatlas_functions.append(module.metric_cluster)
        else:
            logger.debug(
                "No clustering metric was specified in --metric_cluster"
            )
        if len(args.metric_annot) > 0:
            checkatlas_functions.append(module.metric_annot)
        else:
            logger.debug(
                "No annotation metric was specified in --metric_annot"
            )
        if len(args.metric_dimred) > 0:
            checkatlas_functions.append(module.metric_dimred)
        else:
            logger.debug("No dim red metric was specified in --metric_dimred")
    # Create summary by default, it is ran at last so it marks
    # the end of the pipeline
    # This table is then used by the resume option
    checkatlas_functions.append(module.create_summary_table)
    return checkatlas_functions


def run(args: argparse.Namespace) -> None:
    """
    Main function of checkatlas
    Run all functions for all atlases:
    - Clean files list by getting only Scanpy atlas (converted from Seurat
    if necessary)
    - Extract summary tables
    - Create UMAP and T-sne figures
    - Calculate every metrics

    Args:
        args: List of args for checkatlas program
    Returns:
        None
    """

    logger.debug(f"Transform path to absolute:{args.path}")
    args.path = os.path.abspath(args.path)
    logger.debug(f"Check checkatlas folders in:{args.path}")
    folders.checkatlas_folders(args.path)

    logger.info("Searching Seurat, Cellranger and Scanpy files")
    atlas_list = list_atlases(args.path)
    # First clean atlas list and keep only the h5ad files
    (
        clean_atlas_scanpy,
        clean_atlas_seurat,
        clean_atlas_cellranger,
    ) = clean_list_atlases(atlas_list, args.path)
    logger.info(
        f"Found {len(clean_atlas_scanpy)} potential "
        f"scanpy files with .h5ad extension"
    )
    logger.info(
        f"Found {len(clean_atlas_seurat)} potential "
        f"seurat files with .rds extension"
    )
    logger.info(
        f"Found {len(clean_atlas_cellranger)} cellranger "
        f"file with .h5 extension"
    )

    # Put all atlases together in the list
    clean_atlas = dict(clean_atlas_scanpy)
    clean_atlas.update(clean_atlas_cellranger)
    clean_atlas.update(clean_atlas_seurat)

    if len(clean_atlas_cellranger) > 0:
        logger.debug("Install Seurat if needed")
        atlas_seurat.check_seurat_install()

    # Run all checkatlas analysis
    # if args.nextflow == 0:
    logger.info(
        "--nextflow option not found: Run checkatlas workflow "
        "without Nextflow"
    )
    run_checkatlas(clean_atlas, args)
    """ else:
        clean_atlas.update(clean_atlas_seurat)
        logger.info(
            "--nextflow option found: Run checkatlas workflow with Nextflow"
        )
        logger.info(f"Use {args.nextflow} threads")
        run_checkatlas_nextflow(clean_atlas, args) """

    if not args.NOMULTIQC:
        logger.info("Run MultiQC")
        multiqc.run_multiqc(args)


def run_checkatlas_nextflow(clean_atlas, args) -> None:
    """
    Run the checkatlas pipeline by using Nextflow.
    checkatlas_workflow.nf will be run with specific
    parameters.

    Args:
        clean_atlas: List of atlases
        args: List of args for checkatlas program

    Returns:
        None
    """
    checkatlas_workflow.create_checkatlas_worflows(clean_atlas, args)
    script_path = os.path.dirname(os.path.realpath(__file__))
    nextflow_main = os.path.join(script_path, "checkatlas_workflow.nf")
    yaml_files = os.path.join(
        folders.get_folder(args.path, folders.TEMP), "*.yaml"
    )

    # getting the current date and time
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%Y%d%m-%H%M%S")
    report_file = os.path.join(
        folders.get_workingdir(args.path),
        f"Nextflow_report-{current_time}.html",
    )
    timeline_file = os.path.join(
        folders.get_workingdir(args.path),
        f"Nextflow_timeline-{current_time}.html",
    )
    working_dir_nextflow = folders.get_folder(args.path, folders.NEXTFLOW)
    nextflow_cmd = (
        f"nextflow run -w "
        f"{working_dir_nextflow}"
        f" {nextflow_main} -queue-size {args.nextflow} --files "
        f'"{yaml_files}" -with-report {report_file}'
        f" -with-timeline {timeline_file}"
    )
    logger.debug(f"Execute: {nextflow_cmd}")
    script_path = os.path.dirname(os.path.realpath(__file__))
    nextflow_main = os.path.join(script_path, "checkatlas_workflow.nf")
    # Run Nextflow
    os.system(nextflow_cmd)
    logger.debug(f"Nextflow report saved in {report_file}")
    logger.debug(f"Nextflow timeline saved in {timeline_file}")


def run_checkatlas(clean_atlas, args) -> None:
    """
    Run Checkatlas pipeline for all Scanpy and Cellranger objects
    Args:
        clean_atlas: List of atlas
        args: List of args for checkatlas program
    Returns:
        None
    """

    # List all functions to run
    pipeline_functions_scanpy = get_pipeline_functions(atlas, args)
    pipeline_functions_seurat = get_pipeline_functions(atlas_seurat, args)
    logger.debug(
        f"List of functions which will be ran "
        f"for each Seurat atlas: {pipeline_functions_scanpy}"
    )

    # Go through all atls
    for atlas_path, atlas_info in clean_atlas.items():
        atlas_name = atlas_info[0]
        # Load adata only if resume is not selected
        # and if csv_summary_path do not exist
        csv_summary_path = os.path.join(
            folders.get_folder(args.path, folders.SUMMARY),
            atlas_name + SUMMARY_EXTENSION,
        )
        if args.resume and os.path.exists(csv_summary_path):
            logger.debug(
                f"Skip {atlas_name} summary file already "
                f"exists: {csv_summary_path}"
            )
        else:
            if atlas_info[1] == "Seurat":
                seurat = atlas_seurat.read_atlas(atlas_path, atlas_info)
                logger.info(
                    f"Run checkatlas pipeline for {atlas_name} Seurat atlas"
                )
                # Run pipeline functions
                for function in pipeline_functions_seurat:
                    function(seurat, atlas_path, atlas_info, args)
            else:
                adata = atlas.read_atlas(atlas_path, atlas_info)
                # Clean adata
                adata = atlas.clean_scanpy_atlas(adata, atlas_info)
                logger.info(
                    f"Run checkatlas pipeline for {atlas_name} Scanpy atlas"
                )
                # Run pipeline functions
                for function in pipeline_functions_scanpy:
                    function(adata, atlas_path, atlas_info, args)


if __name__ == "__main__":
    path = "/Users/christophebecavin/Documents/testatlas/"
    # atlas_path = "/Users/christophebecavin/Documents/testatlas/"
    atlas_info = ["test_version", "Scanpy", ".h5ad", "data/test_version.h5ad"]
    # folders.checkatlas_folders(path)
    # atlas_list = list_atlases(path)
