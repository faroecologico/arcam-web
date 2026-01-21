import csv
import os

def clean_format():
    input_file = "productos_sin_categoria.csv"
    output_file = "productos_para_recategorizar.csv"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} no existe.")
        return

    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            # Definimos campos claros para la IA
            fieldnames = ['ID', 'Nombre_del_Producto', 'SKU', 'Precio_Actual', 'Ruta_Categoria_Sugerida', 'Notas_IA']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                writer.writerow({
                    'ID': row['id'],
                    'Nombre_del_Producto': row['name'],
                    'SKU': row['sku'],
                    'Precio_Actual': row['price'],
                    'Ruta_Categoria_Sugerida': '', # Espacio para que la IA complete
                    'Notas_IA': '' # Espacio para razonamiento si es necesario
                })

    print(f"Formato corregido. Archivo listo para la IA: {output_file}")

if __name__ == "__main__":
    clean_format()
