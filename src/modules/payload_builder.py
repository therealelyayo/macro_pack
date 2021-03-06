import os
from modules.mp_module import MpModule
import logging
from modules.template_gen import TemplateToVba
from modules.embed_file import Embedder

class PayloadBuilder(MpModule):
    """ Class for modules which are used to generate a file """
    
    def __init__(self,mpSession):
        self.embeddedFilePath = mpSession.embeddedFilePath
        super().__init__(mpSession)    
    
    
        
    def embedFile(self):
        """
        Embed the content of  self.embeddedFilePath inside the generated target file
        """
        raise NotImplementedError
    
    
    def generate(self):
        """ Generate the targeted file """
        raise NotImplementedError
    
    def check(self):
        """ Verify generation feasability return true if ok, false if not"""
        
        raise NotImplementedError
    
    
    def printFile(self):
        if os.path.isfile(self.outputFilePath):
            logging.info(" [+] Generated file content:\n") 
            with open(self.outputFilePath,'r') as f:
                print(f.read())
        
    
    def vbTransformAndObfuscate(self):
        """ Call this method to apply transformation and obfuscation on the content of temp directory """
        return 


    def processDosCommandLine(self,commandLine):
        """ evaluate command line to  separate target and arguments """
        return
    
    def run(self):
        
        logging.info(" [+] Prepare %s file generation..." % self.outputFileType)
        # Check feasability
        if not self.check():
            return
        
        # generate template
        if self.mpSession.template:
            generator = TemplateToVba(self.mpSession)
            generator.run()
        
        # embed a file if asked
        if self.embeddedFilePath:
            generator = Embedder(self.mpSession)
            generator.run()
        # Obfuscate VBA files
        self.vbTransformAndObfuscate()
        # generate
        self.generate()
        
        # Shall we display result?
        if self.mpSession.printFile:
            self.printFile()
        
        