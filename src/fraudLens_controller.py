import os
import cv2
from PIL import Image
import image_verification
from transformers import CLIPProcessor, CLIPModel

# Define directories for saving uploaded files
save_directory = {
    "Passport": r"uploaded\passport",
    "Address Proof": r"uploaded\address_proof",
    "Selfie": r"uploaded\selfie"
}
save_file ={}

def accept_files(document_type, uploadedFile):
    # Specify the directory where you want to save the uploaded files
    if not os.path.exists(save_directory[document_type]):
        os.makedirs(save_directory[document_type])
    # Define the path where the file will be saved
    save_file.update({document_type : os.path.join(save_directory[document_type], uploadedFile.name)})
    # Write the uploaded file to the specified location
    with open(save_file[document_type], "wb") as f:
        f.write(uploadedFile.getbuffer())
    # Process the saved file
    passport_photo = image_verification.extract_passport_photo(save_file[document_type])
    cv2.imwrite("extracted_passport_photo.jpg", passport_photo)

def compare_images():
    passport_embedding = image_verification.extract_face_embedding("extracted_passport_photo.jpg")
   
    selfie_embedding = image_verification.extract_face_embedding(save_file["Selfie"])
    # Ensure that embeddings have the same dimensions
    print(f"Passport embedding shape: {passport_embedding.shape}")
    print(f"Selfie embedding shape: {selfie_embedding.shape}")

    similarity_score = image_verification.calculate_similarity(passport_embedding, selfie_embedding)
    threshold = 0.6  # Define similarity threshold for matching
    context = image_verification.create_match_context(similarity_score, threshold)
    print(context)

    # Step 5: Extract Additional Information from Passport using Vision LLM
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    passport_image = Image.open(save_file["Passport"])
    inputs = processor(images=passport_image, return_tensors="pt")
    outputs = model.get_image_features(**inputs)
    print("Facial similarity score:", similarity_score)
    evaluation_result = image_verification.evaluate_matching(similarity_score, threshold)
    print(evaluation_result)
    return evaluation_result




    
    