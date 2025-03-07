from deepface import DeepFace
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from scipy.spatial.distance import cosine
import cv2
import numpy as np

# Step 1: Extract Photo from Passport Image
def extract_passport_photo(passport_image_path):
    print("extract_passport_photo:::passport_image_path::",passport_image_path)
    """
    Extract the passport photo region from the passport image using OpenCV.
    Args:
        passport_image_path (str): Path to the passport image.
    Returns:
        np.array: Cropped passport photo.
    """
    image = cv2.imread(passport_image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        raise ValueError("No face detected in the passport image.")

    # Assuming the largest detected face is the passport photo
    x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
    passport_photo = image[y:y + h, x:x + w]
    return passport_photo

#passport_image_path = "images/passport/pic7.jpg"
#selfie_image_path = "images/passport/pic8.jpeg"

# Extract passport photo from the passport image
#passport_photo = extract_passport_photo(passport_image_path)

# Save the extracted passport photo for further use
def extract_face_embedding(image_path, model_name='VGG-Face'):
    """
    Extract facial embeddings using DeepFace.
    Args:
        image_path (str): Path to the image.
        model_name (str): DeepFace model to use for extraction.
    Returns:
        np.array: Facial embedding vector.
    """
    embedding_result = DeepFace.represent(img_path=image_path, model_name=model_name)
    # If DeepFace returns a dictionary, extract the embedding value
    if isinstance(embedding_result, list) and isinstance(embedding_result[0], dict):
        embedding = embedding_result[0]['embedding']
    elif isinstance(embedding_result, list):
        embedding = embedding_result[0]
    else:
        embedding = embedding_result
    return np.array(embedding).flatten()

# Step 3: Calculate Similarity Score
def calculate_similarity(embedding1, embedding2):
    """
    Calculate cosine similarity between two embeddings.
    Args:
        embedding1 (np.array): First embedding vector.
        embedding2 (np.array): Second embedding vector.
    Returns:
        float: Similarity score between 0 and 1.
    """
    if embedding1.shape != embedding2.shape:
        raise ValueError(f"Embeddings have different shapes: {embedding1.shape} and {embedding2.shape}")
    return 1 - cosine(embedding1, embedding2)

def create_match_context(similarity_score, threshold):
    """
    Create context based on similarity score.
    Args:
        similarity_score (float): Similarity score between passport and selfie.
        threshold (float): Threshold for determining match.
    Returns:
        str: Contextual message for verification.
    """
    if similarity_score >= threshold:
        return "The passport photo matches the selfie. Proceed with onboarding."
    else:
        return "The passport photo does not match the selfie. Request additional verification."



# Here, outputs can be further processed to generate insights or verify textual data
# Step 6: Evaluation Function for Verification
def evaluate_matching(similarity_score, threshold):
    """
    Evaluate the matching of passport and selfie based on similarity score.
    Args:
        similarity_score (float): Calculated similarity score.
        threshold (float): Similarity threshold.
    Returns:
        str: Evaluation result indicating match or mismatch.
    """
    if similarity_score >= threshold:
        return "Match confirmed. Onboarding can proceed."
    else:
        return "Match not confirmed. Manual verification required."