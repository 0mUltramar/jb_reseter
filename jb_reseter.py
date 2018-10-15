import shutil
import re
import os


class JetBrainsTrialDropper:
    """JetBrains products reseter"""

    def __init__(self, name: str):
        self.home_dir = os.path.expanduser('~')
        try:
            product_pref_name = self._get_product_pref_name(name)
        except IsADirectoryError:
            print('Seems you have no such product: {}'.format(name))
            return
        self.product_dir_name = product_pref_name
        print('Start cleaning: {}'.format(name))

    def run(self):
        """Start process"""
        if not hasattr(self, 'product_dir_name'):
            return
        self._dir_remove()
        self._remove_options_eval()
        print('Done')

    def _get_product_pref_name(self, name: str) -> list:
        """Returns name of a directory with product preferences"""
        files = os.listdir(self.home_dir)
        list_dir = list()
        for file_name in files:
            if re.match('.{}20'.format(name), file_name, re.IGNORECASE) is not None:
                list_dir.append('{}/{}'.format(self.home_dir, file_name))
        if len(list_dir) != 0:
            return list_dir
        raise IsADirectoryError

    def _remove_options_eval(self):
        """Removes options"""
        for prod_dir in self.product_dir_name:
            options_path = '{}/config/options/options.xml'.format(prod_dir)
            re_compile = re.compile('.+evlsprt', re.IGNORECASE)
            print('Replaces eval rows in: {}'.format(options_path))
            try:
                with open(options_path, 'r') as f:
                    lines = f.readlines()
            except FileNotFoundError:
                print('Options file was not found: {}'.format(options_path))
                return
            with open(options_path, 'w') as f:
                for line in lines:
                    if re.match(re_compile, line) is not None:
                        continue
                    f.write(line)

    def _dir_remove(self):
        """Removes bad directories"""
        for prod_dir in self.product_dir_name:
            eval_dir = '{}/config/eval'.format(prod_dir)
            print('Removing dir tree: {}'.format(eval_dir))
            try:
                shutil.rmtree(eval_dir)
            except FileNotFoundError:
                pass
            user_pref_dir = '{}/.java/.userPrefs/jetbrains'.format(self.home_dir)
            print('Removing dir tree: {}'.format(user_pref_dir))
            try:
                shutil.rmtree(user_pref_dir)
            except FileNotFoundError:
                pass


for product in ('phpstorm', 'pycharm', 'goland'):
    jb = JetBrainsTrialDropper(product)
    jb.run()