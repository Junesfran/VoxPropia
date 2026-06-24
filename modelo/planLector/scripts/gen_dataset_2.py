import json
import os

output_file = "/Users/samuel.salcedo/Samuel Salcedo/IA_Big_Data/Voz-propia/VoxPropia/modelo/planLector/dataset_finetune.jsonl"
system_prompt = "Eres un asistente virtual del IES Comercio experto en la biblioteca y las actividades del centro. Respondes de forma clara y amable."

qa_pairs_variations = [
    # ---- LIBROS (Variaciones) ----
    ("Oye, ¿qué me dices de Drácula? Me interesa para leer.", "El clásico 'Drácula' de Bram Stocker lo tenemos en la editorial Anaya. Es de género narrativa y está recomendado para 1º ESO. Sigue a Jonathan Harker durante su terrorífico viaje a Transilvania."),
    ("Estoy en primero de la ESO y quiero engancharme a un libro de fantasía.", "Si te gusta la fantasía, 'Percy Jackson y el ladrón del rayo' de Rick Riordan es genial. Percy descubre que es un semidiós y va en busca del rayo de Zeus junto a sus amigos."),
    ("¿Tenemos algún cómic o novela gráfica que hable de problemas médicos?", "Sí, puedes llevarte 'Ausencias', un cómic autobiográfico de Ramón Rodríguez y Cristina Bueno que trata sobre desmayos epilépticos, para 1º ESO."),
    ("Dime de qué va '50 cosas sobre mí', porfa.", "Es de ficción juvenil escrito por Care Santos y trata de un joven chico relatando el momento cuando, casi sin pensar en tres o cuatro segundos, le salvó la vida a otra persona que no soporta. (2º ESO)."),
    ("Libros sobre ritos y selvas africanas en la biblioteca para 2º ESO.", "Ese sería 'El medallón perdido' de Ana Alcolea, que sumerge a Benjamín en una aventura de autodescubrimiento en la selva de Gabón mientras busca la herencia de su fallecido padre."),
    ("Una novela donde la gente quede encerrada por la nieve.", "'La ratonera' de Agatha Christie es un excelente clásico policial en el que los huéspedes de la mansión Monkswell quedan aislados por la nieve con un asesino. (2º ESO)."),
    ("Profe, me obligan a leer un libro de temas sociales en 3º ESO. ¿Alguno que no sea aburrido?", "Te atrapará 'Deja en paz a los muertos' (J.R. Barat). Un muchacho en vacaciones empieza a sufrir sueños con alguien extraño y una perturbadora amenaza anónima."),
    ("¿De quién es el libro de La memoria del Holocausto?", "El ensayo novelado 'Ana Frank, la memoria del Holocausto' pertenece al autor Eduardo Lozano (Editorial Vicens Vives) y se destina a 3º ESO."),
    ("¿De qué va El Lazarillo de Tormes?", "Narra la azarosa vida de Lázaro, pasando penurias durante el siglo XVI bajo el servicio de distintos amos, todo con un matiz irónico y pícaro. Contamos con la adaptación de Vicens Vives para 3º ESO."),
    ("Novelas románticas pero con algo oscuro para 3º de secundaria.", "Deberías leer 'Desconocidos' de David Lozano. Narra cómo una cita a ciegas se termina conectando misteriosamente con la muerte de un joven indocumentado."),
    ("De qué trata 'La visita del inspector'?", "Es una obra de suspense de J.B. Priestley donde, después de una animada cena de los Birling, todos acaban implicados por un inspector en la repentina muerte de una chica."),
    ("Deseo leer algo que transcurra en 1938.", "'Bala para el recuerdo' de Maite Carranza. Ambientada en ese año, el estudiante Miguel se dispone acompañado de su perra Greta a buscar a su padre a un campo franquista (3º ESO)."),
    ("Sinopsis del libro de Marianela.", "Trata de la dulce pero poco agraciada Marianela, quien cría un sincero romance prestando ayuda a Pablo, ciego de nacimiento. Esto cambia el día que un doctor llega prometiéndole ver la luz."),
    ("Títulos de asesinos de SM para 4º ESO.", "Tenemos 'Donde surgen las sombras' (David Lozano). El protagonista, Álex, es aficionado a las consolas y su preocupante desaparición lleva todo al extremo por culpa de crueles asesinos ocultos."),
    ("De qué va Bodas de sangre.", "En 'Bodas de sangre', escrita por Federico García Lorca (Vicens Vives, 4º ESO), una joven apunto de casarse ve todo desmoronado al aparecer su exnovio dispuesto a retomar la relación."),
    ("Novelas juveniles de Martin Gaite.", "'Caperucita en Manhattan', que reinterpreta en Nueva York la clásica fábula de los bosques usando a la chica Sara Allen, buscando la libertad. Es para 4º ESO."),
    ("De qué año o lugar es Historia de una escalera.", "Trata la vida encajonada en el espacio de treinta años consecutivos experimentada por las humildes familias dentro de la escalera interior de su portal. Del autor A. Buero Vallejo (4º ESO)."),
    ("Quién escribió La mecánica del corazón y su editorial.", "Mathias Malzieu es el autor, traído por Reservoir Books. Literatura asombrosa de 4º ESO acerca del frágil corazón de madera del pequeño Jack."),
    ("Dónde puedo saber los hábitos para alcanzar la plenitud personal?", "Consultando 'La riqueza que el dinero no puede comprar', del famoso Robin Sharma, idóneo para enseñanzas medias y enfocarse al bienestar de estilo de vida armonioso."),
    ("Ciencia Ficción orientada al ejército?", "En efecto, 'Cartas desde el desierto' (Manu Carbajo para 3º/4º ESO) detalla El Desierto, ese punto infame de La Mili al cual trasladan a los más repudiados sociales a cumplir sentencia."),
    ("Autores que hablen del origen de recuerdos y pensamiento.", "Te puedes instruir mediante Aristóteles y otros entrevistados creativos leyendo el volumen '¿Qué pasa en tu cabeza?' de Capogrossi y Macrì (Siruela para 3º ESO)."),
    ("De qué va Memorias Ahogadas.", "Dicho libro de FPGB aborda los destrozos por las memorias y vidas que debieron de ser abandonadas para dar cupo a la construcción forzosa de los embalses a lo largo de nuestro país."),
    ("Título para estudiar desastres como riadas. 2º de BB.", "Puedes leer las causas bajo el manual 'Vivir con el río. Gestión del riesgo de inundación' publicado por Pepitas de Calabaza como aclaratoria sobre desastres igual que el temporal del 2024 de DANA."),
    ("Algo para alumnos de 1º de Formación que sea divertido e histórico.", "Tenemos maravillas divulgativas como 'La Rioja y sus pueblos entre cuentos', por S.H. López-Pastor y G. Álava, incluyendo desde pasatiempos locales a pequeñas comprensiones."),
    ("Cuál es el libro de los ratoncitos en el laberinto.", "Esa excelente narrativa de 1º ACO se titula '¿Quién se ha llevado mi queso?', de Spencer Johnson (Empresa Activa)."),
    ("Qué pinto Velázquez y se relaciona con el plan nuestro de biblioteca?", "'Siete historias para la infanta Margarita'. Creado por Fernández-Pacheco, donde narra invenciones y sucesos ante una de las más grandes figuras, Las Meninas (2º ESO)."),
    ("Ernest Shackleton. Qué tenemos para tercero.", "Ese gran aventurero del sur polar en 1914 inspira el relato 'Endurance, la prisión blanca', de Alfred Lansing. Es narrativa de pura supervivencia para 3º ESO."),
    ("Qué género es Maus.", "Maus pertenece al género 'novela gráfica o cómic'. Es un valioso testimonio generacional del sufrimiento del Holocausto de los padres de Art Spiegelman, enfocado a 4º ESO."),
    ("De qué trata el cómic Persépolis.", "Se trata de un testimonio y duro relato para nivel de 1º Bachillerato analizando el extremismo en el crecimiento islámico vivido por Marjane Satrapi desde dentro en su adolescencia bajo el velo."),
    ("Cuentanos Sawabona.", "Sawabona enfoca el comportamiento del perdón por encima del resentimiento en la comunidad a propósito del descuido de la infantil Themba por el sur africano."),
    ("Un relato de la princesa buscando un esposo.", "Bajo Jorge Bucay dispones de la ingeniosa lección 'La princesa busca marido' la cual pone condiciones durísimas hacia pretendientes exigiendo estar aguantando en la pared al sol"),
    ("¿Aparece algo en inglés o con personajes como Mr. Ripley?", "Patricia Highsmith fue aficionada al suspense, pero por este libro no tenemos material de ella. Sí poseemos relato musical extranjero histórico para 1º ESO 'El amor es ciego' de William Boyd ambientándose entre amor de Brodie y Lika."),
    ("Argumento del tigre y del burro.", "Esa ilustrativa anécdota muestra a dos animales debatiendo sobre una tonta afirmación; quien castigado es quien sabía la realidad, por no haberlo evitado discutiendo tontamente."),
    ("Para 1º de preparatoria de Bachiller busco autoayuda y filosofía.", "Prueba el ameno viaje '¿Hay filosofía en tu nevera?' de Gel. Discurrirás ante incógnitas humanas si posees curiosidad existencial desde elementos digitales actuales."),
    ("Qué narra El escarabajo de oro de Poe?", "'El escarabajo de oro' (1843) entrega tramas de un grandísimo misterio deductivo literario en nuestra edición dirigida especialmente al alumnado del curso 1º ESO."),

    # ---- ACTIVIDADES (Variaciones) ----
    ("Quería detalles de Soria, qué ocurrió.", "En esa bella salida del 20 de marzo de 2026 nos aventuramos tras los pasos originarios de la literatura vinculada entre letras de Antonio Machado para 3º y 4º de E.S.O."),
    ("Estudiantes que charlaron del medio siglo XX.", "Ese grupo estuvo comprendido por miembros de 2º de Bachillerato guiados en la ponencia oral por la talentosa madrileña Marina Casado con motivo de su generación poética."),
    ("De qué fecha es la fiesta de mujeres europea.", "En fechas del entorno al día 8 de marzo. Específicamente el día previo (7 de marzo '25) 1º SAD lanzó pódcast radiados entre la multitud y letreros visualizando la grandeza científica femenina en pasillos."),
    ("Cuál fue la cita pacifista el curso del 26.", "Nos concentramos para finales de Enero rechazando fuertemente el belicismo mundial aportando ilustraciones contra ataques. Resaltaba el texto sobre la paz pacífica Ghandiana."),
    ("Elfos en el aula de letras.", "En el pabellón vecinal SIES, diciembre 2025 presenció desde la OSE el aprendizaje lingüístico decorativo narrando los descuidos de estos minúsculos seres para terminar siendo enmarcados bajo el formato postal de festividad."),
    ("Dónde conversaron con Moreno?", "Bajo la Semana del Valle fuimos partícipes todos nosotros al polideportivo universitario riojano debatiendo de sus famosas obras y de auto pulicaciones (2025)."),
    ("Quién creó el escape WTF.", "Estuvo impulsado e íntegramente desarrollado por la genial plantilla de logísticas de personal 'Rafael Azcona'. Permitiendo fomentar destrezas anti desinformación al curso auxiliar."),
    ("Cuéntame si han adaptado Halloween artísticamente en SIES.", "Recreando Halloween alumnos del SIES tomaron textos góticos rehaciendo esas leyendas narrativas directamente mediante miradas del oscuro personaje protagónico. Apellidando en 25 al invento bajo: The Haunted Gallery."),
    ("Quién visitó desde fuera el comercio en literatura joven?", "El carismático escritor Manu Carbajo interactuando el 17 de noviembre de su exitosísima redacción en las lecciones tras nuestras jornadas reflexivas en nuestro recinto."),
    ("Lázaro y Sheherezade de la oralidad en Octubre 25.", "Pertenecieron a las mágicas mil y una noches contadas majestuosamente al aire por Héctor Urién al atrapar niños 1.º, donde una vida literaria a cada noche duraban de aliento ante su califa."),
    ("Equipos reordenando nuestro banco.", "En un asombroso lio los estudiantes del Con Voz Propia fueron de ayuda fundamental categorizando clásicas vs juveniles y rescatando fichas con sus obras en la actividad del 'Qué es este lío'."),
    ("A qué cine acudieron los premios migrantes.", "Las jóvenes de la escuela obtuvieron tal reconocimiento de los defensores Amnistía ubicadas en nuestra región en el espectacular complejo cines logroteños 'Infantes' un pasado abril."),
    ("Fotocall plástico del Arte en Comercio.", "Fue por el llamado Día a Convivencias donde 2º Taller Educación de nuestra sede facilitó enormes escenarios para enmarcarte vivos al interior de históricos cuadros (abril 25)."),
    ("Intercambio de abril.", "Claro, mediante vales y recogidas para toda nuestra Feria local donamos lecturas escolares al área Departamental de Letras, resultando fenomenal reabastecimiento en la red estudiantil."),
    ("Poemas con banco de libros FP.", "Conocido 'Banco Lector'. Con la fecha 21 de marzo del equinoccio, llenamos cada tabla, y en paralelo, con versos ilustrados por aulas de Ciclos para mostrar emociones literarias escritas 25."),
    ("Visitaron actrices Doña jacinta.", "No es que fuesen actrices de jacinta. Sino nuestras escolares el curso pre navidad del Centro Cultural, aprendiendo mediante una puesta al teatro lo célebre e importancias de mujeres del Logroño de la antigua época (4º y primero B.)"),
    ("Concursos miedo de noviembre", "Como de rigor para Noviembre de Textos montamos el premio 'Terror'. Respondiendo la afición gótica estudiantil con su escalofriante talento por el horror para encuadernarse post fallos hacia una magna Colección local miedosa."),
    ("Buzón Bullying en lector noviembre.", "Como parte Tirar de la Lengua. Los docentes colgaron correspondencia reflexiva para el intimidado 'Alumno Omega', pegando pegatinas con caras a su alrededor por la solidaridad general escolar 24."),
    ("Se vio a Carles García narrando el tonto.", "En octubre del 24 un par de cuentacuentos abordaron la colección Ana Matute de infantes extraños, llamados 'Niños tontos'. Relatado por Zarándula entre ritmos armónicos para respetar diferencias."),
    ("Mérida.", "Insuperable viaje formativo griego o latino bajo nuestro programa donde pisamos las tierras emeritenses en el XXV de abril 2023 por el majestuoso coliseo con comedias teatrales directas en su cuna."),
    ("Cuentos sobre Navidad de Charles Dickens 22.", "Mediante móviles descargaban los PDF de los rincones institucionales completándolo con certamen evaluativo para recompensas durante navidades escolares las seis cuestiones elementales."),
    ("Precio justo y expusición del dinero...", "Nuestras clases de la biblioteca azcona se dividieron investigando cómo de crudo es el dinero bajo niñez sin recursos logrando dinámicas tipo tele 'el precio está bien' guiados por monitores informativos (Octubre 2022).")
]

jsonl_lines = []
for q, a in qa_pairs_variations:
    record = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": q},
            {"role": "assistant", "content": a}
        ]
    }
    jsonl_lines.append(json.dumps(record, ensure_ascii=False))

with open(output_file, 'a', encoding='utf-8') as f:
    f.write("\n" + "\n".join(jsonl_lines))

print(f"Appended {len(qa_pairs_variations)} entries to {output_file}")
