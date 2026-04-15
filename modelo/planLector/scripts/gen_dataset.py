import json
import os

output_file = "/Users/samuel.salcedo/Samuel Salcedo/IA_Big_Data/Voz-propia/VoxPropia/modelo/planLector/dataset_finetune.jsonl"
system_prompt = "Eres un asistente virtual del IES Comercio experto en la biblioteca y las actividades del centro. Respondes de forma clara y amable."

qa_pairs = [
    # ---- LIBROS ----
    ("¿Quién escribió Drácula y para qué curso es?", "Drácula fue escrito por Bram Stocker, publicado por la editorial Anaya, y está recomendado para 1º ESO."),
    ("Recomiéndame un libro de aventuras para 1º ESO.", "Te recomiendo 'Percy Jackson y el ladrón del rayo' de Rick Riordan. Es una apasionante aventura sobre un niño que descubre ser un semidiós."),
    ("¿De qué trata el libro Percy Jackson?", "Cuenta la historia de Percy, un semidiós de 1º ESO que averigua que es hijo de un dios griego. Él, junto a Grover y Annabeth, debe descubrir quién ha robado el rayo de Zeus para evitar una guerra en el Olimpo."),
    ("¿Hay algún cómic autobiográfico sobre salud?", "Sí, 'Ausencias'. Es un cómic de Ramón Rodríguez y Cristina Bueno recomendado para 1º ESO, que cuenta de manera personal su vivencia con desmayos epilépticos."),
    ("¿Para qué edad o curso recomiendan el libro 50 cosas sobre mí?", "El libro '50 cosas sobre mí' escrito por Care Santos (editorial Edebé), está pensado para estudiantes de 2º ESO."),
    ("¿Hay alguna novela juvenil que ocurra en África?", "Sí, 'El medallón perdido' de Ana Alcolea. Transcurre en Gabón, donde Benjamín busca el medallón de su difunto padre."),
    ("¿A qué editorial pertenece El medallón perdido y para qué curso es?", "Es de la editorial Anaya y está enfocado a 2º ESO."),
    ("Me gusta Agatha Christie, ¿qué libro para 2º ESO recomiendas?", "Puedes leer 'La ratonera' de Agatha Christie. La historia narra sobre unos huéspedes de una pensión que quedan incomunicados por la nieve y averiguan que hay un asesino entre ellos."),
    ("Busco libros que tengan un poco de misterio y suspense para 3º ESO.", "Te sugerimos 'Deja en paz a los muertos' de J.R. Barat. Habla de Daniel Villena, quien tiene sueños misteriosos y una escalofriante carta anónima."),
    ("¿Aparece algo relacionado con los nazis en la biblioteca para los de 3º ESO?", "Sí, disponemos de 'Ana Frank, la memoria del Holocausto' de Eduardo Lozano (Vicens Vives). Una rigurosa historia sobre una familia exiliada y recluida en Ámsterdam."),
    ("Hola, busco alguna versión moderna del Lazarillo de Tormes.", "Poseemos la adaptación del 'Lazarillo de Tormes' estructurada por Eduardo Alonso en la editorial Vicens Vives, muy adecuada para 3º ESO."),
    ("Querría que me expliques de qué trata Desconocidos, de David Lozano.", "Es un misterio en el cual dos jóvenes desconocidos quedan para una cita a ciegas, pero paralelamente aparece el cadáver de otro muchacho. Al final, ambos hechos convergen de forma sorprendente."),
    ("Me gustaría leer algo de teatro inglés clásico. Estoy en tercero de la ESO.", "Puedes consultar 'La visita del inspector' de J.B. Priestley. Es una obra donde la familia Birling es investigada de repente por un inspector ante un suicidio, lo que lleva a un enorme debate moral."),
    ("¿Tenéis algo que hable sobre nuestra Guerra Civil o su periodo en la biblioteca?", "Sí, 'Bala para el recuerdo' de Maite Carranza (3º ESO). Es la desgarradora historia de un niño apellidado Miguel, que emprende un largo viaje en 1938 para rescatar a su padre de las prisiones del bando contrario."),
    ("¿Qué es Marianela?", "Marianela es una famosa historia de Benito Pérez Galdós. Es un texto para 4º ESO en el que una humilde chica, lazarillo de Pablo, entra en conflicto cuando él está a punto de dejar la ceguera y ver cómo ella no es tan hermosa."),
    ("Dime un libro sobre de internet y videojuegos, misterio, por favor. Es para 4º ESO.", "Te gustará 'Donde surgen las sombras' de David Lozano. Narra cómo después de que Álex (entusiasta de los videojuegos) desaparezca inexplicablemente, sus compis vivirán atrocidades para entender qué clase de asesino existe detrás."),
    ("Quiero repasar o ver Bodas de Sangre de Lorca.", "Puedes solicitarla. La biblioteca cuenta con 'Bodas de sangre', la emblemática tragedia pasional escrita por Federico García Lorca (Vicens Vives), ideal para 4º de la ESO."),
    ("Me suena un título de Caperucita, pero de ciudad.", "Probablemente te refieras a 'Caperucita en Manhattan', de Carmen Martín Gaite. Adaptación catalogada para 4º ESO donde Sara Allen vive diversas peripecias desde Brooklyn para llevar un pastel a su abuela a Manhattan."),
    ("Historia de una escalera, ¿es un buen libro? ¿para quién?", "Totalmente. Es de A. Buero Vallejo y recomendado en 4º ESO. En él vemos treinta años de vida y lamentos de tres familias diferentes condensados en los peldaños de un mismo escalón de comunidad."),
    ("Cuentos sobre un corazón falso", "Se trata de 'La mecánica del corazón', relato de Mathias Malzieu donde su protagonista tiene dañado el corazón y lo reemplazan por un reloj de madera condicionando cómo lograr el amor verdadero sin estropearlo."),
    ("Dame información de La riqueza que el dinero no puede comprar.", "Es una valiosa obra de autoayuda y desarrollo personal de Robin Sharma (conocido estratega) que promueve 'las 8 formas de riqueza' y sirve idóneamente al grado 3º y 4º de ESO."),
    ("Estoy en 3º ESO. ¿Tienes novela juvenil de tipo distopía?", "Sí, te aconsejo 'Cartas desde el desierto' (Manu Carbajo). Cuenta de unos jóvenes que enfrentan torturas en el espeluznante Servicio Militar del futuro, recluyéndolos en medio de la incomunicación geográfica."),
    ("Libro del cerebro para escolares.", "Pídele al encargado '¿Qué pasa en tu cabeza? El cerebro y la neurociencia' (Siruela). Este manual detalla respuestas a las emociones mediante una especie de entrevista a ilustres personajes históricos que investigaron nuestra mente (3º ESO)."),
    ("Algo en la FPGB de historia española sobre embalses?", "Para nuestro módulo de FPGB CCAA II se encuentra la novela 'Memorias ahogadas'. Indaga rigurosamente y expone los dolorosos testimonios mudos de aquella gente española que de un día a otro abandonó el pueblo al convertirlo el estado dictatorial en un embalse gigante."),
    ("Tenemos material a mano sobre gestión del riesgo por la DANA?", "Tenemos el texto documental 'Vivir con el río. Gestión del riesgo de inundación' redactado para 2º Bachillerato bajo los recientes problemas en Valencia (octubre de 2024). Explora conceptos fluviales serios desde un marco científico entendible."),
    ("¿Tienes lecturas cortas para básica sobre la Rioja?", "Para nuestro Grado Básico (1º SAD) disponemos el formato 'La Rioja y sus pueblos entre cuentos', perfecto para leer curiosidades sobre nuestras costumbres o escudos acompañado de ejercicios visuales."),
    ("Fábula o libro sobre tomar elecciones en épocas cambiantes. Básica.", "Sí. Contamos con '¿Quién se ha llevado mi queso?' que en escasas páginas instruye a personajes enfrentados al arrebato del queso por un laberinto en constantes rediseños (Empresa Activa)."),
    ("Qué historia me cuentas en literatura si la chica se llama Infanta Margarita?", "Tenemos 'Siete historias para la infanta Margarita' de Miguel Fernández-Pacheco, donde se imaginan los divertidos cuentos usados en el siglo XVII para que la rebelde princesita estuviera tranquila modelando Las Meninas."),
    ("Busco algo sobre exploración para un alumno de tercero de la ESO", "Acércate a por 'Endurance, la prisión blanca'. Narra de manera periodística y fascinante la travesía congelada que hizo Shackleton a la Antártida junto a veintisiete hombres, atrapados a bordo de su navío."),
    ("El cómic de los judíos y nazis.", "¿Te refieres a 'Maus'? Es uno de los mejores cómics (4º ESO) realizados. Narra sin pudor la represión judía y se usa un genial formato donde las etnias y naciones son interpretadas vía diversos animales."),
    ("Recomiéndame una novela gráfica biográfica para 1º de Bachillerato.", "Tienes la excelente lectura 'Persépolis'. Muestra el doloroso paso hacia la madurez de su creadora durante toda la guerra en la cual deviene y reprime su antigua religión en la república de Irán."),
    ("Cuento sobre el perdón en otras culturas.", "Sawabona relata los comportamientos compasivos hallados entre una tribu local africana a la hora de restituir el amor y honor por una niña infractora."),
    ("Fábula graciosa del romance.", "Puede serte atractiva 'La princesa busca marido' del psicólogo Jorge Bucay, la ingeniosa parábola que advierta del gran honor que amerita quedarse quieto al borde del palacio, hasta el año justo, para conseguir matrimonio."),
    ("Libro de William Boyd en nuestra IES.", "Se trata de 'El amor es ciego'. Narra la vida entrelazada por un músico errante por París llamado Moncur con una preciosa artista de ópera a través de una incansable persecución alrededor de toda nuestro continente dieciochesco."),
    ("Quiero discutir usando filosofía, soy de Bachillerato.", "Pide el manual 'Filosofía en la calle' (Eduardo Infante) o '¿Hay filosofía en tu nevera?' (Enric F. Gel). Disponen el modo perfecto actual para relacionarnos mentalmente a pensadores tan genios usando redes y nuestra rutina cotidiana."),
    ("¿Tenemos El Principito en el IES Comercio?", "Desde luego. Pertenece a nuestra lista de 1º de ESO y corresponde a la editorial Salamandra, aborda un viaje astral metafórico para curar la adultez."),
    ("Cuentos sobre detectives de Poe en español", "En castellano para 1º ESO encuentras 'El escarabajo de oro' el maravilloso invento donde arranca nuestra fascinante corriente en relación de crímenes deductivos que inventaron el formato policial."),
    ("Quiero un clásico americano en inglés adaptado a Secundaria.", "Ahí contamos a título Burlington de 'The Adventures of Tom Sawyer' (Mark Twain), en base al famoso y descarado chicuelo a través del Mississipi."),
    ("Tenéis 'The Indian in the Cupboard'?", "Sí, en versión anglosajona dirigida a los niveles 2º ESO. Con un contenido muy emocionante de una mesa convertidora que propicia transformar plástico a materia consciente."),
    ("Me recomienden novela gráfica en idioma para secundaria 3.", "En esta aula puedes seleccionar la edición inglesa 'Smile'. Muestra a Raina en la edad tonta frustrada a raíz de todo el ridículo del aparato de sus dietes con extraños eventos accidentales."),
    ("Thriller literario en inglés para los de 4.", "Puedes pedir en la biblioteca The Secret of the Lake, de autor Liz Trenow. Indaga misterios post WWII de Gran Bretaña sobre una joven con infortunios y trágicos secretos bajo el lago que encubre a un vecino ahogado."),
    ("Tenemos the Great Gatsby.", "Se tiene constancia en esta biblioteca recomendándolo para 1º Bachillerato."),
    ("Una novela donde la protagonista tenga aparato y se rompa los dientes?", "'Smile' de Raina Telgemeier. Una novela gráfica genial y algo angustiosa (para 3º ESO) sobre lidiar con ortodoncias larguísimas y sismos juveniles."),

    # ---- ACTIVIDADES ----
    ("¿Cuándo se hará la ruta por el camino de Antonio Machado?", "Realizamos este hermoso sendero poético 'La ruta machadiana' para alumnos desde 3º, 4º de ESO hasta 1º de Bachillerato el pasado 20 de marzo (2026). Visitando calles mágicas y paisajes literarios presenciales de forma activa para que no sólo queden los poemas impresos."),
    ("Quien expuso los textos de Marina Casado en el instituto?", "La mismísima Marina Casado aportó nuestra actividad en marzo 26 sobre los llamados 'Poetas del medio siglo' logrando maravillar y enseñar este momento a estudiantes de los dos niveles de Bachillerato durante su amena y pedagógica explicación."),
    ("Mencionarme de qué fueron las actividades del día internacional de la paz 2026.", "Logramos celebrar a final de Enero una bonita confluencia de todos para rechazar un nuevo auge del conflicto militar y la necesidad pacífica dibujando nuestras aportaciones anti misiles de nuestro colegio. "),
    ("Qué organizaron en Nochebuena o Navidades en SIES con elfos?", "Alumnos del SIES usaban el cuento de travesuras para practicar reglas idiomáticas que han estudiado los cursos primeros de la OSE con el sentido navideño. Las travesuras las reformulaban para que parecieran suyas antes de presentarlas a color."),
    ("Eventos especiales por el Día de la Biblioteca a 25 oct.", "Realizamos una macro conmemoración del Día de Biblioteca toda la anterior semana al cierre mes, donde se repartieron cómics escalofriantes, ambientamos espacios del colegio inspirándonos del terror a mano de proyectos PIE con voz Propia."),
    ("Cómo participamos como Comercio en el Valle de la Lengua?", "Fletamos grupo para marchar al polideportivo literario. El gran invitado para charlar fue Eloy Moreno a nuestros alumnos pre universitarios, lo que propició dedicatorias autografiadas de la trayectoria de sus exitosas obras."),
    ("Tuvimos Escape Room?", "En conjunto a la enorme gestión de 'Rafael Azcona' hicimos participar de 'WTF! Escape room' un lúdico laberinto de 'desinformación' y destreza analítica al alumnado grado de FP para alcanzar con criterio el carnet inmunitario fuera sus cúpulas confinadas para noviembre (25)."),
    ("El relato o autor de terror para Navidades fue Manu?", "Manu Carbajo vino más bien a principios (Octubre '25). Hablando de su obra la cual habían devorado y debatido predeciblemente los discípulos obteniendo respuestas vitales respecto el arte y diseño narrativo."),
    ("De qué manera se vio y trabajó 'Las mil y una noches'", "Atraídos al misterio oral por el intérprete Héctor Urién, el que mantuvo encandilado con peripecias y filosofía que salvaban la cabeza de una noche a la protagonista exótica Sheherezade."),
    ("Concurso del día del migrante 2025, qué paso?", "¡Maravilloso! Fue organizado el IES ganando y reivindicando las dolorosas memorias internacionales del Amnistía de Derechos junto con las excelentes de nivel autonómicas como Aya, Alaia y Irene bajo cines riojanos el ocho de Abril."),
    ("Compañeros, la 'Feria del Libro' se hizo este abril de comercio?", "El IES celebró en Abril en nuestras zonas céntricas la brillante 'Feria del Libro'. Repartiendo cupones para el trueque escolar masivo para poder entregar ejemplares del ciclo leído por lecturas y literatura siguiente totalmente gratuito."),
    ("En FP gestionamos el mes de la mujer?", "Nuestro alumnado del CFGM Gestión de Administraciones logró preparar en sus pódcast durante 'Mujeres europeas de la huella', así expusieron de igual forma como de las pasadas personalidades (Wolf Virginia o Chanel o Curies) por todo banco hasta el pódcast para recreo."),
    ("Hubo alguna cosa que hicieron con Slimm1.", "Apareció por clases de Grado FP nuestro exitoso 'whodafuckslimm1', un informático graduado el mismo colegio y rapero impartiendo sesiones rítmicas e improvisadas del uso lírico con versos de los pupilos a puro disfrute juvenil."),
    ("Alguien ha ido o hizo 'Profesiones sin género'?", "Alumna Plástica y profesores como Carmen Llorente dirigieron la concientización temprana de desigualdades ocupacionales rompiendo tabús que han impuesto desde un análisis con nuestros grupos nacientes desde 1º Secundaria."),
    ("Hubo arte con grabados?", "Sí, guiado bajo ilustrador genio Aitor Espié logramos instruir talleres a jóvenes de Artes en la azcona, replicando sus propios estampados luego colgados con gratitud nuestra."),
    ("¿Qué pasó con los concursos de terror en noviembre?", "Al confluir mes tenebroso y literatura para alumnos creamos cuentos inéditos como recompensa recopilados posteriormente a la antología."),
    ("¿A qué iba la famosa iniciativa de nuestro Alumno Omega?", "Como rechazo definitivo del terrible Bullying en 2024. A través de este sistema anónimo y misivas reflexivas pedimos y calificamos aportes anímicos desde Banco Literatura al público."),
    ("Qué calendario han de resolver las navidades literario?", "Tuvimos dos años el peculiar Advento. Destreza detective cada 24 d as descubriendo de a una cita qué clásico original contenía y a qué gran mente pergeñada. Aquellos más certeros se lucían regalos locales o vales cafetería."),
    ("El teatro Mar sobre tsunamis, lo vieron en el IES?", "A nuestro pesar trata una dramática historia a la rebeli n e introspección por el luto del suicido en parientes bajo estéticas pasionales que generaron fuerte controversia, admiración dolorosa entre 2024 las salas del visionado externo"),
    ("Quién actuaba Los niños tontos?", "Eran las obras sentimentales sobre singularidad escritoras de Matute representadas verbal por Carles (Zarándula), bajo suave acompañamiento al armonio de Jiménez el primer octubre, reivindicando un colegio desde respeto generalizado."),
    ("Alguien se unió alguna vez en olimpiadas Solidarias", "Durante pasadas desgracias como la primera intervención total a la pobre Ucrania, a cada minuto usado bajo los libros por estudiante logramos en COOPERA costear un valor benéfico enorme recaudando gracias decenas estudiantes comprometidos solidaria en su currículo normal."),
    ("Fuisteis la expediciones a Mérida o Latín?", "Para homenajear humanidades clásicas de todo comercio nuestra comitiva de filología Clásicos presenció dentro su afamadísimo certamen europeo nada inferior que Sófocles en pleno gigantesco complejo ruinero del sur y del mismo coliseo ibérico en (Abril 23)."),
    ("Han tocado Cuentos sobre Dickens Navidad?", "Tanto que en el último certamen dictamos en Navidades concursos para quienes devorasen los PDF con seis sencillas peripecias o cuestionarios navideñas respondiéndoles una serie vales de regalos."),
    ("Leímos de Shackleton algo de teatro o charla?", "La biblioteca y los relatores del equipo pasaron la asombrosa leyenda antártica para ejemplificar de que con enorme coraje ni hielo pudo arrebatar a ese barco 'Endurance' ninguna vida. Lo presenciaron tercer curso."),
    ("Hicieron grabaciones los del Día de Miedo o Biblioteca?", "No. Sin embargo el premio poesía digital 'post-esía' solicitaba formato vídeopoemas. También organizaron lecturas como micrófonos de radio pero usualmente nos contentan redactar y enmarcarlos mediante concursos literarios como El Terror o Amar el San Valentín"),
    ("Algún fotocall raro?", "Nuestro 'Fotocall Formas Parte de una Arte'. El taller pintó siluetas que evocaban genios universales pictóricas hasta conseguir asombrar en 2025 al alumnado por la diversión de los estudiantes para el día convivencia escolar local")
]

jsonl_lines = []
for q, a in qa_pairs:
    record = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": q},
            {"role": "assistant", "content": a}
        ]
    }
    jsonl_lines.append(json.dumps(record, ensure_ascii=False))

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(jsonl_lines))

print(f"File created with {len(qa_pairs)} entries at {output_file}")
