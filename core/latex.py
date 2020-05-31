
class Latex:
    def __init__(self, ssh):
        """
            latex
        """
        self.bash = ssh.bash


        self.compiler = 'pdflatex'

    def compile(self, path,src):
        try:
            r = self.bash.run('cd {} && {} {}'.format(path, self.compiler, src))
            return r
        except:
            print("PDFLATEX ERROR")
            raise
        return True