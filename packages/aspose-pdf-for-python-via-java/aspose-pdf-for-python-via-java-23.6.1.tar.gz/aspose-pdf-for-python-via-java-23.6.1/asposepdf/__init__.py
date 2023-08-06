import jpype
import os

__version__ = "23.6.1"
__version_info__ = __version__.split('.')
__asposepdf_dir__ = os.path.dirname(__file__)
__pdf_jar_path__ = __asposepdf_dir__ + "/jlib/aspose.pdf-python-23.4.jar"
jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" % __pdf_jar_path__)
__all__ = ['Assist', 'Api', 'Device', 'Forms', 'PdfFileEditor', 'Facade']
