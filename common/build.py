
class Build:
    def __init__(self, bash, src_dir, build_dir,repo, branch, owner):
        """
        coucou
        """


        self.git = {'repo':repo, 'branch':branch}
        self.bash = bash
        self.srcDir = src_dir
        self.buildDir = build_dir
        self.owner = owner


        self.pre_build()
        self.setup_git_env()
        self.post_build()

    def pre_build(self):
        self.bash.mkdir(self.srcDir)
        self.bash.mkdir(self.buildDir)
        self.bash.chown(owner   = '{}:wheel'.format(self.owner), 
                        pattern = self.srcDir)

    def post_build(self):
        b=0


    def setup_git_env(self):
        print("\n\n==> setup_git_env\n\n")
        if  not self.bash.directory_exists(self.srcDir + '/.git'):
            self.bash.clone(branch  = self.git['branch'], 
                            repo    = self.git['repo'], 
                            pattern = self.srcDir)
                        
        result = self.bash.reset(branch  = self.git['branch'], 
                               pattern = self.srcDir)