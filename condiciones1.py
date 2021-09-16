dni = int(input('ingrese DNI: '))

puedeSubir = False

if dni % 2 == 0:
  puedeSubir = True
  print('Puede subir es = ', puedeSubir)

else:
  puedeSubir = False
  print('No puede subir', puedeSubir)
    