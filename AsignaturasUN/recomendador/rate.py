import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import GridSearchCV
from recomendador.models import Asignatura, Calificacion

def recomendacion(usuario):
    array = []
    for rate in Calificacion.objects.all():
        array.append([rate.usuario_id, rate.asignatura_id, rate.calificacion])
    
    df = pd.DataFrame(data=array)
    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(df, reader)
    trainingSet = data.build_full_trainset()
    param_grid = {
        'n_factors':[50,100,150],
        "n_epochs": [40,50,60],
        "lr_all": [0.002, 0.005],
        "reg_all": [0.4, 0.6]
    }

    gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=3)
    gs.fit(data)
    #Parametros optimos
    params = gs.best_params["rmse"]
    SVDoptimized = SVD(n_factors=params['n_factors'], n_epochs=params['n_epochs'],lr_all=params['lr_all'], reg_all=params['reg_all'])
    SVDoptimized.fit(trainingSet)

    asig = Asignatura.objects.all()

    asig_user = Calificacion.objects.all().filter(usuario_id = usuario.id)

    #Asignaturas sin calificar
    asignaturas_SinC = []
    for asignatura in asig:
        encontrado = False
        for asignatura_usuario in asig_user:
            if (asignatura_usuario.asignatura_id == asignatura.codigo):
                encontrado = True
        if (not encontrado):
            asignaturas_SinC.append(asignatura)

    #asignaturas_recomendados
    asignaturas_rec = []

    for asignatura in asignaturas_SinC:
        asignaturas_rec.append({'asignatura': asignatura, 'svd': SVDoptimized.predict(usuario.id, asignatura.codigo).est})
    # A function that returns the 'year' value:
    def ordenador(e):
        return e['svd']
    
    asignaturas_rec.sort(reverse=True, key=ordenador)

    return asignaturas_rec