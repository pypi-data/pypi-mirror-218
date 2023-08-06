from pathlib import Path
import pytest
from pydra.tasks.mrtrix3.utils import MRConvert
from medimages4tests.dummy.dicom.mri.dwi.siemens.skyra.syngo_d13c import (
    get_image as get_dwi_dicom,
)
from medimages4tests.dummy.nifti import get_image as get_nifti


@pytest.fixture
def dwi_dicom_dataset():
    return get_dwi_dicom()


@pytest.fixture
def nifti_dataset(work_dir):
    return get_nifti(work_dir / "nifti", compressed=True)


def test_mrconvert_default_out_file(nifti_dataset):

    task = MRConvert(in_file=nifti_dataset, axes=[0, 1, 2, -1])

    result = task()

    assert Path(result.output.out_file).exists()


@pytest.mark.xfail(
    reason=(
        "Cannot pass input to input field with 'output_file_template' "
        "https://github.com/nipype/pydra/pull/585 (or equivalent) is merged "
        "into main branch"
    )
)
def test_mrconvert_explicit_out_file(dwi_dicom_dataset):

    task = MRConvert(in_file=dwi_dicom_dataset, out_file="test.nii.gz")

    result = task()

    assert Path(result.output.out_file).exists()
