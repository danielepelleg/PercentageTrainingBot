from texttable import Texttable

def draw_table(number):
    """
        Draw percentages table.
    """
    percentages = [50, 53, 55, 57, 60, 62, 63, 65, 66, 67, 68, 70, 72, 73, 75, 77, 76, 78, 80, 82, 85, 87, 88, 90, 95, 97, 98, 102, 105, 107]
    records = [['%', 'Weight']] # Headers

    for p in percentages:
        weight = round(float(p*number/100), 2)
        records.append([f'{p}%', f'{weight:.2f}\tKg'])

    # Table Creation
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.add_rows([row for row in records])

    return f"```{table.draw()}```"