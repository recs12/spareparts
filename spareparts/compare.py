#! python3
#2019-03-27 by recs
# ===check the current owner of type licenses===
#
import click
import pandas as pd

# p = Path('.')
# list_of_spls = [f.name for f in p.glob('*.xls*') if not f.name.startswith('~')]


def extract_items_auto(file):
    """
    Extraction column: item number
    """
    data = pd.read_excel(file, sheet_name='Sheet1', header=0, usecols="A", dtype={0:str})
    data['Item Number'] = data['Item Number'].str.strip()
    data = data.dropna(how='all')
    serie = pd.Series(data['Item Number'])
    serie = serie.unique().tolist()
    return set(serie)

def extract_items_manual(file):
    """
    Extraction column: item number
    """
    data = pd.read_excel(file, sheet_name='Data', header=0, usecols="A", dtype={0:str})
    data.columns = ['items']
    data['items'] = data['items'].str.strip()
    data = data.dropna(how='all')
    serie = pd.Series(data['items'])
    serie = serie.unique().tolist()[1:]
    return set(serie)

def parsing_items(spl):
    name_file = str(spl)
    if name_file.startswith('std'):
        return extract_items_manual(name_file)
    elif name_file.startswith('auto'):
        return extract_items_auto(name_file)
    else:
        print(f'[Warning] file name: {spl} not reconized, file should start with auto.. or std..' )
    
def delta(spl1, spl2):
    return (
        sorted(list(parsing_items(spl1) - parsing_items(spl2)))
        )

@click.command()
@click.argument('spl1', nargs=1)
@click.argument('spl2', nargs=1)
def main(spl1, spl2):
    click.echo(spl1)
    click.echo(spl2)
    s = pd.Series(
        delta(spl1, spl2)
    )
    s.to_csv('difference.txt', index=False)

if __name__ == '__main__':
    main()