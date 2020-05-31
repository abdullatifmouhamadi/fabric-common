
class Build:
    def __init__(self, bash, code_dir, repo, branch, owner):
        """
        coucou
        """


        self.git = {'repo':repo, 'branch':branch}
        self.bash = bash
        self.codeDir = code_dir
        self.owner = owner


        self.pre_build()
        self.setup_git_env()
        self.post_build()

    def pre_build(self):
        self.bash.mkdir(self.codeDir)
        self.bash.chown(owner   = '{}:wheel'.format(self.owner), 
                        pattern = self.codeDir)

    def post_build(self):
        b=0


    def setup_git_env(self):
        print("\n\n==> setup_git_env\n\n")
        if  not self.bash.directory_exists(self.codeDir + '/.git'):
            self.bash.clone(branch  = self.git['branch'], 
                            repo    = self.git['repo'], 
                            pattern = self.codeDir)
                        
        result = self.bash.reset(branch  = self.git['branch'], 
                               pattern = self.codeDir)