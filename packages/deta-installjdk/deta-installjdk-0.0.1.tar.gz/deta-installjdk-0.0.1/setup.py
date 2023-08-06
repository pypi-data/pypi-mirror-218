from setuptools import setup
from setuptools.command.install import install
import jdk

def installjdk():
    print("[JAVA]: Installing jre...")
    path = jdk.install('18', jre= True)
    print("[JAVA]:   done!\n[JAVA]: Path to jre is: {}".format(path))

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        installjdk()

setup(
    name='deta-installjdk',
    version='0.0.1',
    description='Attempts to install a JRE and prints the binary path.',
    install_requires=[
        'install-jdk',
    ],
    cmdclass= {
        'install': PostInstallCommand,
    },
)