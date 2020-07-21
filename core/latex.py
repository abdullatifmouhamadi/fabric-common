
class Latex:
    def __init__(self, ssh):
        """
            latex
        """
        self.bash = ssh.bash


    # https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile#latex-recipe
    #pdflatex -> bibtex -> pdflatex X 2

    # Recipe step 1
    # 
    def compile(self, path, src):
        try:
            #compiler = "-pdf" # -pdflatex
            compiler = "-xelatex" # -xelatex
            r = self.bash.run('cd {} && latexmk {} -synctex=1 -interaction=nonstopmode -file-line-error {}.tex -outdir="."'.format(path, compiler, src))
            #r = self.bash.run('cd {} && latexmk -synctex=1 -interaction=nonstopmode -file-line-error -pdf -g {}.tex -outdir="."'.format(path, src)) force 'g' parma
            #r = self.bash.run('cd {} && bibtex {}'.format(path, src))
            #r = self.bash.run('cd {} && pdflatex -synctex=1 -interaction=nonstopmode -file-line-error {}'.format(path, src))
            #r = self.bash.run('cd {} && pdflatex -synctex=1 -interaction=nonstopmode -file-line-error {}'.format(path, src))
            return r
        except:
            print("PDFLATEX ERROR")
            raise
        return True