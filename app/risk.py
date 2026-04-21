def calcular_nivel_riesgo(probabilidad, impacto):
    riesgo = probabilidad * impacto
    if riesgo >= 15: return riesgo, 'Crítico'
    if riesgo >= 10: return riesgo, 'Alto'
    if riesgo >= 5:  return riesgo, 'Medio'
    return riesgo, 'Bajo'


def calcular_riesgo_residual(riesgo_inherente, salvaguardas):
    if not salvaguardas:
        return riesgo_inherente
    eficacia_media = sum(s.eficacia for s in salvaguardas) / len(salvaguardas)
    return round(riesgo_inherente * (1 - eficacia_media / 100), 2)


def resumen_riesgos(riesgos):
    resumen = {'Crítico': 0, 'Alto': 0, 'Medio': 0, 'Bajo': 0}
    for r in riesgos:
        nivel = r.nivel_riesgo
        resumen[nivel] += 1
    return resumen
