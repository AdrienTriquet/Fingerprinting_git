from ravif import ravif
from recallage import recallage
import cv2
from correlation import f_correlation


def frame_out_of_video(video_path):
    # La fonction recallage prend 2 images en entrées
    # On prend une frame au milieu des videos pour comparer (optimisation réalisable)
    # Opens the Video file
    cap = cv2.VideoCapture(video_path)

    list_frames = []
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        # Passage sous niveaux de gris ?
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        list_frames.append(frame)

    # on prend la frame du milieu
    long = len(list_frames)
    nb_inter = int(long / 2)

    # Pour l'appel dans la fonction de 'script' il faut une image, pas un numpy array
    # On doit donc réécrire l'image en jpg par ex
    path = 'image_travail/' + str(video_path) + '.jpg'
    # path = "image_travail"
    cv2.imwrite(path, list_frames[nb_inter])

    return path
    # return list_frames[nb_inter]


def global_fonction(video_base, video_compar):
    # On commencer par prendre une frame pour le recallage
    path_frame_base = frame_out_of_video(video_base)
    path_frame_compar = frame_out_of_video(video_compar)

    recal = recallage(path_frame_base, path_frame_compar)
    angleDeg = recal[0]
    scaleFactor = recal[1]
    X = recal[2]
    Y = recal[3]

    # S'il y a une rotation, on test la correlation avec et sans rotation
    if angleDeg != 0:

        fingerprint_base = ravif(video_base, 0, 0)
        print('on its way : 1/5')
        fingerprint_compar = ravif(video_compar, X, Y)
        print('on its way : 2/5')

        correl = f_correlation(fingerprint_base, fingerprint_compar)
        print('on its way : 3/5')

        fingerprint_compar = ravif(cv2.rotate(video_compar, angleDeg), X, Y)
        print('on its way : 4/5')

        new_correl = f_correlation(fingerprint_base, fingerprint_compar)

        if new_correl[0] > correl[0]:
            correl = new_correl

    else:
        fingerprint_base = ravif(video_base, 0, 0)
        print('on its way : 1/3')
        fingerprint_compar = ravif(video_compar, X, Y)
        print('on its way : 2/3')

        correl = f_correlation(fingerprint_base, fingerprint_compar)

    if correl[0] < 0.9:
        return 'Done : Pas de correlation forte : ' + str(correl[0])

    return 'Done : Correlation forte : ' + str(correl[0])


video_base = "video_travail/A.mp4"
video_compar = "video_travail/B.mp4"

print(global_fonction(video_base, video_compar))
