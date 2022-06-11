from argparse import ArgumentParser
import sys, os

cli_parser = ArgumentParser(description="init project or add page", prog="tk_up", usage='%(prog)s', allow_abbrev=False,)

cli_subParsers = cli_parser.add_subparsers(title='Commande', dest='C')

# INIT

command_init = cli_subParsers.add_parser('init', help='Init project')

command_init.add_argument('-folder', type=str, help='select your folder page')

# ADD

command_add = cli_subParsers.add_parser('add', help='add page')
command_add.add_argument('NamePage', type=str, help='name page')


# command_add.add_argument('-fd', '-function_disable', action='store_true')
# command_add.add_argument('-fe', '-function_enable', action='store_true')

# VERSION

group = cli_parser.add_mutually_exclusive_group()
group.add_argument('-v', '--version', action='version', version="V1")

# parse

cli_args = cli_parser.parse_args()

# print(cli_args)

if cli_args.C == None:
    cli_parser.print_help()
    sys.exit("\nOne argument expected")

path_exe = os.getcwd()
path_tempalte = f"{os.path.dirname(os.path.realpath(__file__))}/template.tmpl"

def init_project():
    pass

def add_page(name:str):

    name = name.lower()
    template: str

    with open(f"{path_tempalte}", "r") as file:
        template = file.read()
        file.close()

    template = template.replace("TEMPLATE_NAME_WIDGET", name)

    with open(f"{name}.py", "a") as file:
        file.write(template)
        file.close()

if __name__ == "__main__":
    if cli_args.C == "add":
        add_page(cli_args.NamePage)