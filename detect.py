from deepface import DeepFace
import json

class FaceDetection:

    def __init__(self, path_to_image, model=None):
        self.path = path_to_image
        if model is not None:
            self.model = model

    def run_model(self):
        return DeepFace.analyze(img_path = self.path)

    def analyse_image(self):
        self.result = self.run_model()
        if self.result:
            try:
                self.emotion_details = self.result[0]['emotion']
                self.emotion = self.result[0]['dominant_emotion']
                self.emotion_confidence = int(self.emotion_details[self.emotion])
                self.face_region = self.result[0]['region']
                self.race_details = self.result[0]['race']
                self.race = self.result[0]['dominant_race']
                self.race_confidence = int(self.race_details[self.race])
                self.gender = self.result[0]['dominant_gender']
                self.gender_confidence = self.result[0]['gender'][self.gender]

                return json.dumps({
                    'emotion_details': {'emotion': self.emotion,
                                        'confidence': self.emotion_confidence,
                                        'analysis': self.emotion_details},
                    'face_details': {'bbox': self.face_region},
                    'race_details': {'race': self.race,
                                    'confidence': self.race_confidence},
                    'gender_details': {'gender': self.gender,
                                    'confidence': self.gender_confidence}
                })
            except (IndexError, KeyError) as e:
                print(f"Error processing result: {e}")
                return json.dumps({'error': 'Result tuple is malformed'})
        else:
            print("No face detected in the image")
            return json.dumps({'error': 'No face detected in the image'})
        

        



    def view_image(self):
        pass 





#f=open("C:\Users\Atchaya\Desktop\ruby\path2.txt","r")


#Face = FaceDetection(path_to_image = f.read())
#result = Face.analyse_image()
#print(result)