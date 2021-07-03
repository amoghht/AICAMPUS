from project.utils import *
from scipy.spatial.distance import cosine
import face_recognition
from numpy import expand_dims
from project import face_encoder
import time


class Camera():
    def gen_frames(camera_status='release_camera'):
        start = 1
        if camera_status == 'open_camera':
            camera = cv2.VideoCapture(0)
            frame_count = 0
            while frame_count <= 100:
                success, frame = camera.read()
                frame_count += 1
                if not success:
                    camera.release()
                    cv2.destroyAllWindows()
                    break
                else:
                    ret, buffer = cv2.imencode(".jpg", frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')







    def fr_face_detect(img):
        model = 'hog'
        scale = 0
        img_converted = img[:, :, ::-1]
        #t0 = time.time()
        face_locations = face_recognition.face_locations(img_converted, number_of_times_to_upsample=scale, model=model)
        #t1 = time.time()
        #print(f'took {round(t1 - t0, 3)} to detect {len(face_locations)} faces')

        return face_locations

    def get_embedding(model, face_pixels):
        # scale pixel values
        face_pixels = cv2.resize(face_pixels, (160, 160))

        face_pixels = face_pixels.astype('float32')

        # standardize pixel values across channels (global)
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        # transform face into one sample
        samples = expand_dims(face_pixels, axis=0)
        # make prediction to get embedding
        yhat = model.predict(samples)
        return yhat[0]

    def face_recognise(face, encoder, known_encodings_dict, recognition_t=0.25):

        encode = Camera.get_embedding(encoder, face)
        encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
        distance = float("inf")
        for db_name, db_encode in known_encodings_dict.items():
            dist = cosine(db_encode, encode)
            if dist < recognition_t and dist < distance:
                name = db_name
                distance = dist
                return name, distance

    def face_recogniser(start_face_recognition='stop_recognition'):
        camera=None
        encodings_path = 'project/data/encodings/encodings1.pkl'
        encoding_dict = load_pickle(encodings_path)
        prev_frame_time = 0
        new_frame_time = 0
        if start_face_recognition == 'start_recognition':
            camera = cv2.VideoCapture(0)

        while camera:
            success, frame = camera.read()
            new_frame_time = time.time()
            if not success:
                pass
            else:
                face_locations = Camera.fr_face_detect(frame)
                if face_locations:
                    (top, right, bottom, left) = face_locations[0]
                    face = frame[top - 40:bottom, left:right]
                    try:
                        predicted_name, cosine_distance = Camera.face_recognise(face, encoder=face_encoder,
                                                                                known_encodings_dict=encoding_dict)
                        for (top, right, bottom, left) in face_locations:
                            cv2.rectangle(frame, (left, top - 40), (right, bottom), (80, 18, 236), 2)
                            cv2.putText(frame, predicted_name + f'__{cosine_distance:.2f}', (left, top - 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 200, 200), 2)

                    except:
                        cv2.putText(frame, 'unknown', (left, top - 50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255), 2)
                fps = 1 / (new_frame_time - prev_frame_time)
                prev_frame_time = new_frame_time
                cv2.putText(frame, str(fps), (50, 50), cv2.FONT_HERSHEY_SIMPLEX ,1,
                            (255, 0, 0), 1)
                ret, buffer = cv2.imencode(".jpg", frame)
                frame = buffer.tobytes()
                if start_face_recognition=='stop_recognition':
                    camera.release()
                    ret, buffer = cv2.imencode(".jpg", frame)
                    frame = buffer.tobytes()
                    cv2.destroyAllWindows()
                    break
                else:
                    pass
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')





    def face_recogniser_get_name():
        encodings_path = 'project/data/encodings/encodings1.pkl'
        encoding_dict = load_pickle(encodings_path)
        predicted_name ='unknown'
        camera = cv2.VideoCapture(0)
        number_of_frame =0

        while predicted_name == 'unknown' and number_of_frame<=100:
            success, frame = camera.read()
            number_of_frame += 1
            if not success:
                pass
            else:
                face_locations = Camera.fr_face_detect(frame)
                if face_locations:
                    (top, right, bottom, left) = face_locations[0]
                    cv2.rectangle(frame, (left, top - 40), (right, bottom), (80, 18, 236), 2)
                    face = frame[top - 40:bottom, left:right]
                    try:
                        predicted_name, cosine_distance = Camera.face_recognise(face, encoder=face_encoder,
                                                                                known_encodings_dict=encoding_dict)

                    except:
                        pass

                if predicted_name != 'unknown':
                    camera.release()
                    cv2.destroyAllWindows()
                    break

        if number_of_frame==100:
            print(predicted_name)
            camera.release()
            cv2.destroyAllWindows()

        return predicted_name



    def register_face(person_name):
        endimage=cv2.imread('project/static/images/thank_you.jpg')
        retendimage, bufferendimage = cv2.imencode(".jpg", endimage)
        endimage = bufferendimage.tobytes()


        encodes = []
        encodings_path = 'project/data/encodings/encodings1.pkl'
        opened_encoding_dict = load_pickle(encodings_path)
        camera = cv2.VideoCapture(0)
        no_of_face = 0
        new_frame=0
        previous_frame=0

        while no_of_face <= 20 :
            ret, frame = camera.read()
            new_frame=frame
            if not ret:
                print("no frame:(")
                break
            try:
                face_locations = Camera.fr_face_detect(frame)
                if face_locations:
                    for (top, right, bottom, left) in face_locations:
                        cv2.rectangle(frame, (left, top - 55), (right, bottom + 5), (80, 18, 236), 2)
                        face = frame[top - 55:bottom+5, left:right]
                        #cv2.imshow('face', face)

                        try:
                            encode = Camera.get_embedding(face_encoder, face)
                            encodes.append(encode)
                            no_of_face += 1
                        except:
                            print("encodings did not capture")
            except:

                print("no face detected ")

            retimage, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()



            try:
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except:
                break
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + endimage + b'\r\n')
        print(f"total embeddings taken from {no_of_face} faces")

        if encodes:
            encode = np.sum(encodes, axis=0)
            encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
            opened_encoding_dict[person_name] = encode
        with open(encodings_path, 'bw') as file:
            pickle.dump(opened_encoding_dict, file)
        print("encodings saved")





