from ravif import ravif
from recalage import recalage
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

    recal = recalage(path_frame_base, path_frame_compar)
    print("recallage =")
    print(recal)
    angleDeg = recal[0]
    scaleFactor = recal[1]
    X = recal[2]
    Y = recal[3]

    #if X != 0:
        #X = (1920 / 2) + X

    #if Y != 0:
        #Y = (1080 / 2) + Y
    # 1920*1080 est la taille d'image en entrée
    # Dacallage ne doit pas être de plus de la moitié de l'image ce qui est le cas avec notre dataset
    #X = int((1920 / 2 + X) * 256 / 1920)
    #Y = int((1080 / 2 + Y) * 256 / 1080)

    X = max(X, -X) * 256 / 1920
    Y = max(Y, -Y) * 256 / 1080
    

    # S'il y a une rotation, on test la correlation avec et sans rotation
    if angleDeg != 0:

        fingerprint_base = ravif(video_base, 128, 128)
        print('on its way : 1/5')
        fingerprint_compar = ravif(video_compar, X, Y)
        print('on its way : 2/5')

        correlation = f_correlation(fingerprint_base, fingerprint_compar)[0]
        print('on its way : 3/5')

        fingerprint_compar = ravif(cv2.rotate(video_compar, angleDeg), X, Y)
        print('on its way : 4/5')

        new_correl = f_correlation(fingerprint_base, fingerprint_compar)

        if new_correl[0] > correlation:
            correlation = new_correl[0]

    else:
        fingerprint_base = ravif(video_base, 128, 128)
        print('on its way : 1/4')
        fingerprint_compar_translate = ravif(video_compar, X, Y)
        print('on its way : 2/4')
        fingerprint_compar_center = ravif(video_compar, 128, 128)
        print('on its way : 3/4')

        correl_translate = f_correlation(fingerprint_base, fingerprint_compar_translate)
        print("correl_translate")
        print(correl_translate)

        correl_center = f_correlation(fingerprint_base, fingerprint_compar_center)
        print("correl_center")
        print(correl_center)

        correlation = max(correl_translate[0], correl_center[0])

    if correlation < 0.8:
        return 'Done : Pas de correlation forte : ' + str(correlation)

    return 'Done : Correlation forte : ' + str(correlation)


video_base = "video_travail/droit_noir.mp4"
video_compar = "video_travail/envers_noir.mp4"

print(global_fonction(video_base, video_compar))
