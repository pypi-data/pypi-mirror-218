from comics_ocr.comics_ocr import ComicsOCR

__author__ = 'Gürkan Soykan'
__email__ = 'grkansoykan@gmail.com'
__version__ = '0.1.0'

# module level doc-string
__doc__ = """
COMICS OCR
================

Description
-----------
ComicsOCR is a Python package created for easily distributing OCR models trained for golden age of comics.

Example
-------
>>> # Import library
>>> from comics_ocr import ComicsOCR
>>> # Initialize
>>> e2e_ocr_model = ComicsOCR(self,
                 ocr_detector_config="/scratch/users/gsoykan20/projects/mmocr/work_dirs/fcenet_r50dcnv2_fpn_1500e_ctw1500_custom/fcenet_r50dcnv2_fpn_1500e_ctw1500_custom.py",
                 ocr_detector_checkpoint='/scratch/users/gsoykan20/projects/mmocr/work_dirs/fcenet_r50dcnv2_fpn_1500e_ctw1500_custom/best_0_hmean-iou:hmean_epoch_5.pth',
                 recog_config='/scratch/users/gsoykan20/projects/mmocr/work_dirs/master_custom_dataset/master_custom_dataset.py',
                 ocr_recognition_checkpoint='/scratch/users/gsoykan20/projects/mmocr/work_dirs/master_custom_dataset/best_0_1-N.E.D_epoch_4.pth',
                 det='FCE_CTW_DCNv2',
                 recog='MASTER'): 
>>> # Run the model
>>> text, preprocessed_text, sanitized_text = model.extract_text(img_path)

References
----------
* https://github.com/gsoykan/comics_text_plus

"""