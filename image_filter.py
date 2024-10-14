import threading
from PIL import Image, ImageFilter
import time
import os

def process_image(image_path, output_path):
    try:
        start_time = time.time()
        print(f"Starting processing {image_path} at {start_time}")
        
        # Verificando se o arquivo existe
        if not os.path.exists(image_path):
            print(f"Error: {image_path} not found.")
            return
        
        # Abrindo e processando a imagem
        image = Image.open(image_path)
        filtered_image = image.filter(ImageFilter.GaussianBlur(5))  # Exemplo de filtro
        
        # Convertendo para RGB caso esteja em RGBA
        if filtered_image.mode == 'RGBA':
            filtered_image = filtered_image.convert('RGB')
        
        filtered_image.save(output_path)
        
        end_time = time.time()
        print(f"Finished processing {image_path} at {end_time}, time taken: {end_time - start_time}s")
    
    except Exception as e:
        print(f"An error occurred while processing {image_path}: {e}")

# Criando threads para processar imagens em paralelo
image1_thread = threading.Thread(target=process_image, args=("image1.png", "output1.jpg"))
image2_thread = threading.Thread(target=process_image, args=("image2.jpg", "output2.jpg"))

# Iniciando as threads
image1_thread.start()
image2_thread.start()

# Esperando todas finalizarem
image1_thread.join()
image2_thread.join()

print("Both images processed.")
