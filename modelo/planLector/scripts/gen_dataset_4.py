import json

output_file = "/Users/samuel.salcedo/Samuel Salcedo/IA_Big_Data/Voz-propia/VoxPropia/modelo/planLector/dataset_finetune.jsonl"
system_prompt = "Eres un asistente virtual del IES Comercio experto en la biblioteca y las actividades del centro. Respondes de forma clara y amable."

qa_pairs_creative_2 = [
    # ---- LIBROS (Variaciones creativas parte 2) ----
    ("Oye amig@, ¿tenéis de casualidad Drácula? Quería releerlo por aquello de los vampiros.", "¡Claro que sí! Bram Stocker nos dejó este clasicazo que tenemos recomendado para el grupo de 1º de ESO bajo la publicación de Anaya. Te enganchará seguro la pesadilla en Transilvania."),
    ("Tengo a mi sobrina que odia leer pero le gusta el cine de superhéroes tipo Marvel o así...", "Enseñale 'Percy Jackson y el ladrón del rayo'. Va de adolescentes descubriendo poderes divinos al ser hijos de dioses en pleno siglo XXI. Está catalogada de fantasía y aventuras para 1º ESO y se devora súper rápido."),
    ("Me aburro mazo. Busco algo rarísimo de un corazón mecánico o de reloj.", "No es rarísimo sino poético: 'La mecánica del corazón' de Mathias Malzieu. Es de 4º ESO, vas a seguir los frágiles pasos de Jack tratando de sobrevivir sin enfadarse ni amar para no reventar su máquina interna."),
    ("Dime un cómic para mí, estoy en 1º ESO y paso un poco de las típicas novelas, quiero dibujos.", "Para tu nivel puedes leer 'Ausencias', dibujado por Cristina Bueno. Aporta un lado autobiográfico, de salud y algo de la vida musical de Ramón Rodríguez superando desmayos epilépticos."),
    ("Hola, soy la madre de un alumno de 2º y quiero un libro realista sobre los adolescentes de hoy, porque son muy raros.", "La obra idónea es '50 cosas sobre mí', un libro de ficción juvenil con tono super espontáneo escrito por la genial Care Santos para segundo de la ESO."),
    ("¿Tenemos cosas sobre fantasmas, médiums y gente en los sueños?", "Sí, puedes encontrar esos matices en la obra de J.R. Barat 'Deja en paz a los muertos'. Recomendada los alumnos de 3º, donde un ser misterioso se entromete perturbando el plácido verano y el sueño de Daniel Villena."),
    ("No sé si haya cosas de Holanda en los años 40. Sobre la represión.", "En nuestra biblioteca ubicamos 'Ana Frank, la memoria del Holocausto' de Lozano, libro vital y desgarrador ambientado en el opresivo Ámsterdam nazi para clases de 3º."),
    ("Dime una comedia romántica típica de 'se conocen por internet' o algo así jiji.", "No es una comedia de internet, pero 'Desconocidos' narra la intriga amorosa moderna del encuentro casual a ciegas en redes que acaba solapada con crímenes mortales (3º de Secundaria de David Lozano)."),
    ("Chaval, de verdad recomiendas el teatro español antiguo para 4º?", "Te asombrará lo actuales que son. 'Bodas de sangre', sin ir más lejos, aborda un triángulo amoroso, y te aseguro que Lorca condensa todo un salseo letal y pasión para hacer volar el escenario por los aires."),
    ("Algo que pase en un edificio con la misma escalera durante décadas.", "Por supuesto. Ocurre dentro de 'Historia de una escalera' (Antonio Buero Vallejo). Refleja dolor y vivencias cruzadas entre progenitores maduros y juveniles esperanzas destrozadas, para el último curso ESO."),
    ("Dime para filosofía alguna locura estilo memes pero profunda.", "Para chicos de 1º Bach, '¿Hay filosofía en tu nevera?' es un libro alucinante donde descubres a Enric F. Gel uniendo internet, cotidianidad y Sócrates, respondiendo el sentido de todo."),
    ("Tienes algo distópico así tipo Black Mirror con soldados adolescentes?", "Tienes que venir a por 'Cartas desde el desierto' (Manu Carbajo para 3-4 ESO) con relatos crudos de la supervivencia anti-sistema bajo El Desierto en 'La Mili' obligatoria."),
    ("¿Aparece algo en inglés de misterio por un lago o asesinato?", "Ese título clave de Reino Unido para cuarto es The Secret of the Lake, a través de la perspectiva tensa y enmudecida de lo ocurrido a una chica de la Inglaterra posguerra persiguiendo el extraño misterio tras su hermano."),
    ("Novelas gráficas para 3", "Seguro amarás el tebeo gringo original titulado Smile donde a la pobre de Rainia le suceden transeuntes graciosísimos e incómodos intentado que sus piños enderezadotes la vuelvan en popular de doce años."),
    ("Busco un libro de autoayuda, me siento estancado con mi desarrollo este tercer grado de colegio.", "Contamos en nuestras repisas con una obra increíble de liderazgo vital, 'La riqueza que el dinero no puede comprar', redactada para guiarte como hace Robin Sharma con estrellas u otra gente."),
    ("Quiero repasar o adentrarme en historia contemporánea y el holocausto no desde lo nazi alemán puro, tal vez de Polonia.", "Puedes tomar el brillante estilo comiquero de Art Spiegelman sobre Vladek, un valiente prisionero del horror que cruzó Polonia. Todo ilustrado y publicado llamándose Maus (4º)."),
    ("Profe, me gustaría algo muy infantil o tierno sobre perdonar.", "Pues contamos en Sawabona, cuentos bajo la cálida bondad de tribus surafricanas redimiendo de cariño a las jóvenes infantiles desde el tacto y el afecto en sus errores. Por Desirée Acevedo lógicamente."),

    # ---- ACTIVIDADES (Variaciones creativas parte 2) ----
    ("Oye, los del B y del C se piraron a Soria el otro día, a qué fueron?", "No fue el otro día sino el reciente veinte de marzo del veintiséis. Viajó nuestro alumnado en plena 'ruta machadiana', absorbiendo aquellos ambientes sorianos tan determinantes y profundos entre la creación natural de Antonio Machado (3º, 4º y Bach.)"),
    ("Me dijeron que trajeron a Marina Casado, y mi madre es re fan de esa profesora.", "Vino en persona como invitada del curso a deslumbrar nuestra mañana de mediados Marzo (13 del 26). Y nos maravilló con su dominio divulgativo a 2º Curso por su literatura del 'Medio Siglo' promoviendo diálogo participado y cercano con nuestros jóvenes lectores."),
    ("En qué quedó lo de la Paz, vi postales en los recreos y por ahí?", "Así nos aliñamos alumnos como el valioso profesorado creando activismo ilustrativos visual e intergeneracional promoviendo convivencias y postales del cese a cruentas batallas a costa de rechazar de cuajo la violencia, este pasado Día Escolar Mundial finalizando Enero."),
    ("Tuvimos unos escape rooms?", "En la Biblioteca ciudadana fuimos el debut inicial para la sala 'WTF!', buscando inocular vacunas 'carne de inmunidad', desenredando a la vez montajes virales o fakes por puro aprendizaje de FP Administrativos y juego cruzado en nuestro pasado noviembre 25."),
    ("Mi hijo vino re asustado de los carteles de Halloween. ¿Qué hicisteis en Comercio?", "Ambientamos espeluznantemente, por y para alumnos de Primer D, nuestro Banco bajo miradas perturbadoras del mítico Pennywise o Cthulhu hasta apellidarle 'Terror en Banco Lector' el de octubre veinticinco."),
    ("De veras Eloy Moreno pisó Logroño?", "Lo trajimos de honor con el 'Semana Valle de Lengua' en la poli de la UR charlando distendidamente ante sus jóvenes lectores de ESO e impresionado para siempre y firmando bolígrafos verdes por el veinte veinticinco (Noviembre)."),
    ("Y con los milenarios cuentos sirios qué habéis hecho.", "Llevamos fascinados a los nuestros de E.S.O. a por la voz alucinante cuentista en escena a Héctor Urién, contando vida tras la genial e ingeniosa de Shariar con Sheherezade a octubre (2025)."),
    ("Alguien reacomodó las cajas y el lío en nuestra aula biblioteca...", "Teníamos al excelente agrupamiento 'Con Voz Propia' desentrañando montañas dispares entre viejas editoras desde lo juvenil a ficción decidiendo al unísono cuál merecían las vitrinas con la actividad de Qué lío por octubre."),
    ("Dieron un premio literario a los nuestros del I.E.S. por ser emigrantes?", "Por la redacción sentida Amnistía Escolar de Migrantes 'Recuerda una vez..', las genias Alaia, Irene, o Aya vencían con orgullo regional entre Logroño durante inicios 2025 su primer medalla a la dignidad."),
    ("Cómo fue eso de sacarse una foto dentro de un cuadro del siglo antiguo?", "Ocurrió al organizar la festividad convicencia por la iniciativa en abril del Fotocall. Nuestros maravillosos integrantes reprodujeron obras grandes por los de Plástica para que pudiésemos integrarnos todos por horas de jolgorio."),
    ("Oye asistenta, le daban un libro gratis a quien llevara un trasto de casa?", "Totalmente; la campaña de Trueque o 'Feria del Libro'. Un simple cupo se entregaba dando sus leídos hacia obtener la lectura gratuita obligatorias próximas en las aulas por fin abril (25)."),
    ("Vinieron chicas y autoras a la megafonía este día mujer de 25?", "Para conmemorar el ocho de Marzo, además colgaron exposiciones valiosas al descanso, nuestras grandes escolares en el grado administrativo publicaron por audios sus 'podcasts' sobre mentes europeas rompedoras entre los recesos dictados."),
    ("Tuvimos música Hip Hop urbana? Que pasada!!", "Nos engalanó con presencia formativa e intensa 'whodafuckslimm', nuestro antiguo y ahora músico DAM enseñando de poética urbana el enero de 2025 con las secciones básicas del FP Comunicaciones."),
    ("Que onda con esas publicidades sobre sin género en las profesiones", "Son geniales letreros y debates organizados gracias Carmen hacia igualdades tempranas frente al desdén general. Rompimos cánones demostrando por las galerías que nuestras futuras mujeres y niños lograran ejercer de oficios no estereotipados para el mañana próspero."),
    ("Aitor Espié es ilustrador de libros verdad?", "Y grandísimo genio, traído gracias la Rafael a nuestra materia visual inculcando qué pasos tiene la profesión creando estampados por él con nuestros encantadores nenes en plástica a otoño pasado (24)."),
    ("Hubo cartas raras en nuestra escuela por el Bullying no?", "Fueron 'Cartas Omega'. Con la empatía a flor pudimos descoser en Noviembre (24) todo daño psíquico mediante estas correspondencias sinceras sobre banco lector logrando erradicaciones reales a esas violentadas mentes atormentadas."),
    ("Cual concurso regalaba desayunos respondiendo famosos autores", "O también recompensado por material libre escolar, el divertidísimo y esperado para diciembre del Adviento donde descubrimos las ocultísimos e interrogantes frases y procedencias hasta ganar las semanas festivas (Citas Célebres)."),
    ("Contaron el libro Navideño de Fantasmas para dar regalos en invierno?", "La biblioteca lanzó aquel sorteazo por navidades pasaditas en 2022 del clásico de Cuento, para quienes lograran acertarle el cuestionario mandando un correo para llevar premios materiales de papelería en base Dickens."),
    ("Ganamos medallas compitiendo estudiando en vez de deporte?", "¡Sí!, Olimpiadas a base del estudio por las cuales nuestro talento financiara bajo COOPERA 1 euro las asolados rincones internacionales como nuestro respaldo Ucrania juntándonos mas de 100 participes."),
    ("Fuiste de viaje al anfiteatro con latín", "Gozábamos por festival de Mèrida los del grecolatin la pasada festividad formativa entre Sófocles asimilando gloriosa historia frente a las imponentísimas y deslumbrantes gradas del esplendoroso Museo antiguo en toda Extremadura.")
]

new_lines = []
for q, a in qa_pairs_creative_2:
    record = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": q},
            {"role": "assistant", "content": a}
        ]
    }
    new_lines.append(json.dumps(record, ensure_ascii=False))

with open(output_file, 'a', encoding='utf-8') as f:
    f.write("\n" + "\n".join(new_lines))

print(f"Appended {len(qa_pairs_creative_2)} creative entries (part 2) to {output_file}.")
