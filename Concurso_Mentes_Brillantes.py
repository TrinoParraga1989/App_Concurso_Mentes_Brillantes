import streamlit as st
import random
import re
from difflib import SequenceMatcher

# ==============================================================================
# BANCO DE 100 PREGUNTAS: FILOSOFÍA PARA MENTES BRILLANTES (1º BACHILLERATO)
# TEMAS: Ética, Lógica, Identidad, Libre Albedrío, Política, Epistemología, 
# Existencialismo, Filosofía de la Ciencia, Mente y Conciencia, Tiempo y Realidad.
# ==============================================================================
questions = [
    {"q": "¿Cuál es la rama de la filosofía que estudia la acción humana en términos de lo que es correcto e incorrecto?",
     "a": "Ética (o Filosofía Moral)",
     "keywords": ["etica", "filosofia", "moral"],
     "context": "La Ética es la rama teórica que examina los fundamentos de la moralidad y la acción correcta."},
    {"q": "¿Cuál es la diferencia principal entre un principio ético y una ley?",
     "a": "Los principios éticos son reglas autoimpuestas o universales; las leyes son normas coercitivas impuestas por una autoridad estatal.",
     "keywords": ["autoimpuestas", "coercitivas", "normas", "leyes"],
     "context": "La Ética se enfoca en el deber interno, mientras que la ley se enfoca en la coerción externa."},
    {"q": "¿Qué es un dilema moral?",
     "a": "Una situación en la que dos o más principios morales entran en conflicto, haciendo imposible cumplir uno sin violar el otro.",
     "keywords": ["dilema", "conflicto", "principios", "moral"],
     "context": "El dilema radica en que no hay una solución fácil o universalmente 'correcta' ya que siempre se viola un valor."},
    {"q": "¿Qué sistema ético se centra en el deber y las reglas universales (como no mentir), independientemente de las consecuencias?",
     "a": "Deontología (asociada a Immanuel Kant).",
     "keywords": ["deontologia", "kant", "deber", "reglas"],
     "context": "La Deontología deriva del griego *deon* ('deber') y establece que ciertas acciones son inherentemente correctas o incorrectas."},
    {"q": "¿Qué sistema ético evalúa la moralidad de una acción basándose únicamente en sus resultados o consecuencias (el fin justifica los medios)?",
     "a": "Consecuencialismo (o Utilitarismo).",
     "keywords": ["consecuencialismo", "utilitarismo", "consecuencias", "resultados"],
     "context": "El Consecuencialismo determina la moralidad de un acto por la cantidad de bien que produce."},
    {"q": "¿Cuál es la regla fundamental del Utilitarismo clásico (Jeremy Bentham)?",
     "a": "Buscar la mayor felicidad para el mayor número de personas.",
     "keywords": ["felicidad", "mayor", "numero", "bentham"],
     "context": "El utilitarismo busca maximizar el bienestar general, considerando a todos los afectados por la acción."},
    {"q": "¿Qué son los valores morales?",
     "a": "Cualidades de las acciones o personas que las hacen deseables o dignas de aprecio (ej. justicia, honestidad, respeto).",
     "keywords": ["valores", "cualidades", "aprecio", "deseables"],
     "context": "Los valores morales guían la conducta y la toma de decisiones, promoviendo el bien social e individual."},
    {"q": "¿La moralidad es absoluta (universal e inmutable) o relativa (dependiente de la cultura o el individuo)?",
     "a": "Es una de las grandes disputas filosóficas; el Absolutismo dice que es fija, el Relativismo dice que es variable.",
     "keywords": ["disputa", "absolutismo", "relativismo", "fija", "variable"],
     "context": "El Absolutismo postula reglas universales; el Relativismo sostiene que las normas cambian según el contexto cultural o histórico."},
    {"q": "¿Cómo se llama el proceso de pensar cuidadosamente sobre un dilema moral para tomar una decisión?",
     "a": "Juicio Moral o Toma de Decisiones Éticas.",
     "keywords": ["juicio", "moral", "decision", "etica"],
     "context": "El juicio moral es la capacidad de discernir entre lo correcto y lo incorrecto en situaciones concretas."},
    {"q": "¿Qué es una virtud según la ética de Aristóteles?",
     "a": "Un rasgo de carácter adquirido que es moralmente bueno, generalmente ubicado en el 'justo medio' entre dos extremos (vicios).",
     "keywords": ["virtud", "aristoteles", "caracter", "justo medio"],
     "context": "Para Aristóteles, la virtud es el hábito de elegir el equilibrio entre el exceso y la deficiencia."},
    {"q": "¿Qué es la Lógica?",
     "a": "La rama de la filosofía que estudia los principios de la inferencia y el razonamiento válido.",
     "keywords": ["logica", "inferencia", "razonamiento", "valido"],
     "context": "La Lógica proporciona las herramientas para determinar si un argumento está bien construido o es falaz."},
    {"q": "¿De qué tipo de razonamiento la conclusión se sigue necesariamente de las premisas (si las premisas son verdaderas, la conclusión debe ser verdadera)?",
     "a": "Razonamiento Deductivo (va de lo general a lo particular).",
     "keywords": ["deductivo", "general", "particular", "necesariamente"],
     "context": "En la deducción, la validez se garantiza por la estructura lógica del argumento, como en un silogismo."},
    {"q": "¿De qué tipo de razonamiento la conclusión es solo probable y se basa en la observación de casos particulares?",
     "a": "Razonamiento Inductivo (va de lo particular a lo general).",
     "keywords": ["inductivo", "probable", "particular", "general"],
     "context": "La Inducción es fundamental en la ciencia, donde se infieren leyes generales a partir de la observación de fenómenos repetidos."},
    {"q": "¿Qué es una falacia?",
     "a": "Un argumento que parece válido, pero contiene un error lógico y es, por lo tanto, inválido.",
     "keywords": ["falacia", "argumento", "error", "invalido"],
     "context": "Las falacias son errores de razonamiento que a menudo se utilizan de forma intencional para persuadir, aunque carezcan de solidez lógica."},
    {"q": "La falacia que ataca a la persona que presenta un argumento, en lugar del argumento en sí, se llama...",
     "a": "Ad Hominem ('contra el hombre').",
     "keywords": ["ad hominem", "ataca", "persona"],
     "context": "El ataque personal desvía la atención del mérito lógico del argumento que se está discutiendo."},
    {"q": "La falacia de petición de principio o razonamiento circular consiste en...",
     "a": "Utilizar la conclusión del argumento como una de sus premisas (asumiendo lo que se intenta probar).",
     "keywords": ["circular", "peticion", "principio", "conclusion", "premisa"],
     "context": "Esta falacia no prueba nada porque la verdad de la conclusión ya estaba asumida en el inicio."},
    {"q": "¿Cuáles son los dos componentes básicos de la estructura de un argumento lógico?",
     "a": "Premisas (las razones) y Conclusión (la afirmación que se intenta probar).",
     "keywords": ["premisas", "conclusion", "razones"],
     "context": "Las premisas ofrecen apoyo a la conclusión, que es el punto principal que el argumento busca establecer."},
    {"q": "¿Qué es una premisa?",
     "a": "Una afirmación que se presenta como apoyo o evidencia para la conclusión.",
     "keywords": ["premisa", "afirmacion", "apoyo", "evidencia"],
     "context": "Una premisa debe ser aceptada como verdadera para que el argumento pueda llevar a una conclusión lógica."},
    {"q": "¿Un argumento con premisas verdaderas y conclusión verdadera es siempre un argumento válido?",
     "a": "No necesariamente; la validez solo se refiere a la estructura lógica del argumento, no a la verdad de su contenido.",
     "keywords": ["no", "validez", "estructura", "logica"],
     "context": "La validez es una propiedad formal; la solidez requiere que el argumento sea válido Y que las premisas sean verdaderas."},
    {"q": "¿Cómo se llama la ley lógica que establece que toda proposición es verdadera o falsa, y no existe un punto intermedio?",
     "a": "Principio del Tercero Excluido.",
     "keywords": ["tercero", "excluido", "proposicion", "falsa"],
     "context": "Este principio clásico de la lógica garantiza que no hay una tercera opción de valor de verdad."},
    {"q": "¿Cuál es el problema filosófico central de la Identidad y el Yo?",
     "a": "Determinar qué es lo que hace que una persona en un momento dado sea la misma persona en otro momento (continuidad).",
     "keywords": ["identidad", "yo", "continuidad", "misma"],
     "context": "El debate se centra en si la identidad reside en el cuerpo, la memoria o alguna sustancia inmaterial."},
    {"q": "¿Qué teoría sostiene que la identidad personal persiste a lo largo del tiempo debido a la continuidad de la conciencia y la memoria?",
     "a": "Teoría Psicológica (asociada a John Locke).",
     "keywords": ["psicologica", "locke", "conciencia", "memoria"],
     "context": "Según Locke, 'Yo' soy quien puedo recordar haber sido."},
    {"q": "Si una persona sufriera amnesia total, ¿qué criterio de identidad se pondría en riesgo, según Locke?",
     "a": "La Identidad Personal (la memoria de ser uno mismo).",
     "keywords": ["identidad", "amnesia", "memoria", "riesgo"],
     "context": "Sin memoria, la conexión psicológica con el pasado se rompe, desafiando la teoría de Locke."},
    {"q": "¿Qué es la identidad corporal?",
     "a": "La idea de que la identidad personal reside en la continuidad y persistencia del mismo cuerpo físico.",
     "keywords": ["corporal", "continuidad", "cuerpo", "fisico"],
     "context": "Esta teoría enfrenta problemas cuando el cuerpo cambia drásticamente o con la posibilidad de trasplantes de cerebro."},
    {"q": "¿Qué pensador propuso la idea del Yo como una colección de percepciones en constante cambio, negando una sustancia única y permanente?",
     "a": "David Hume.",
     "keywords": ["hume", "coleccion", "percepciones", "cambio"],
     "context": "Hume vio el 'Yo' no como una cosa, sino como un 'paquete' o 'haz' de experiencias transitorias."},
    {"q": "¿Qué significa la identidad numérica?",
     "a": "Que dos cosas son literalmente una y la misma cosa.",
     "keywords": ["numerica", "misma", "cosa", "literalmente"],
     "context": "Es la forma más estricta de identidad; se opone a la identidad cualitativa, donde dos cosas son similares."},
    {"q": "En la filosofía oriental, particularmente en el budismo, el concepto de Anatta (no-yo) implica que...",
     "a": "No existe un Yo permanente, inmutable e independiente.",
     "keywords": ["anatta", "bdismo", "no-yo", "inmutable"],
     "context": "Esta postura niega la existencia de un alma o esencia fija que persista a través del tiempo."},
    {"q": "¿Qué es el Self (el Yo) en la filosofía contemporánea?",
     "a": "El centro unificado de la experiencia, la voluntad y la conciencia de uno mismo.",
     "keywords": ["self", "yo", "centro", "unificado", "conciencia"],
     "context": "El Yo es el sujeto que tiene la capacidad de reflexionar y actuar en el mundo."},
    {"q": "¿Cuál es el problema de la 'nave de Teseo' aplicado a la identidad?",
     "a": "¿Si se reemplazan todas las partes de un objeto (o persona) con el tiempo, sigue siendo el mismo objeto (o persona)?",
     "keywords": ["teseo", "reemplazan", "partes", "mismo"],
     "context": "Este dilema ilustra la tensión entre los criterios corporal y psicológico de la identidad."},
    {"q": "¿Cómo influyen los roles sociales y las interacciones en la formación de la identidad, según algunas teorías modernas?",
     "a": "Argumentan que el Yo es en gran medida una construcción social y relacional.",
     "keywords": ["construccion", "social", "relacional", "roles"],
     "context": "El Yo no es una entidad aislada, sino que se moldea a través de la interacción con la sociedad."},
    {"q": "¿Qué postula el Determinismo Fuerte?",
     "a": "Que todas las acciones y eventos son el resultado inevitable de causas anteriores y, por lo tanto, el libre albedrío es una ilusión.",
     "keywords": ["determinismo", "fuerte", "inevitable", "ilusion", "causas"],
     "context": "El Determinismo Fuerte niega cualquier posibilidad de que la persona 'pudiera haber actuado de otra manera'."},
    {"q": "¿Qué es el Libre Albedrío?",
     "a": "La capacidad de un agente para elegir genuinamente entre dos o más cursos de acción alternativos (el agente 'podría haber actuado de otra manera').",
     "keywords": ["libre", "albedrio", "elegir", "alternativos", "cursos"],
     "context": "Es la creencia en que la voluntad humana es la causa primera de las propias acciones."},
    {"q": "¿Qué postura afirma que el Libre Albedrío y el Determinismo son compatibles?",
     "a": "Compatibilismo (o Determinismo Suave).",
     "keywords": ["compatibilismo", "suave", "compatibles"],
     "context": "Los compatibilistas redefinen la libertad, a menudo como la capacidad de actuar según los propios deseos, aunque estos deseos estén determinados."},
    {"q": "¿Cuál es la implicación principal de la negación del libre albedrío en la vida social y legal?",
     "a": "La responsabilidad moral y la justificación del castigo legal se vuelven problemáticas o insostenibles.",
     "keywords": ["responsabilidad", "moral", "castigo", "problematicas"],
     "context": "Si las personas no eligen, no pueden ser culpables ni merecedoras de castigo en sentido estricto."},
    {"q": "¿Qué sostiene el Incompatibilismo?",
     "a": "Que el Libre Albedrío y el Determinismo se excluyen mutuamente; si uno es verdad, el otro es falso.",
     "keywords": ["incompatibilismo", "mutuamente", "excluyen"],
     "context": "Esta postura afirma que son visiones opuestas de la causalidad de la acción humana."},
    {"q": "¿El Indeterminismo implica necesariamente el libre albedrío?",
     "a": "No, el indeterminismo solo significa que los eventos son aleatorios, no que sean elegidos por un agente consciente.",
     "keywords": ["indeterminismo", "aleatorios", "no", "agente"],
     "context": "Para ser libre albedrío, la acción debe ser causada por el agente, no por el azar."},
    {"q": "¿Cómo se relacionan las leyes de la física con el determinismo?",
     "a": "Las leyes físicas universales a menudo se citan como la base del determinismo: dada la condición inicial, solo hay un resultado posible.",
     "keywords": ["leyes", "fisica", "base", "resultado"],
     "context": "El determinismo cosmológico se apoya en la idea de que todas las interacciones están regidas por leyes naturales fijas."},
    {"q": "¿Qué papel tiene la elección en el debate entre libre albedrío y determinismo?",
     "a": "Para el libre albedrío, la elección es la causa; para el determinismo, la elección es el efecto inevitable de causas previas.",
     "keywords": ["eleccion", "causa", "efecto", "inevitable"],
     "context": "La elección es el punto de conflicto: ¿es un origen o un eslabón en la cadena causal?"},
    {"q": "¿Qué se entiende por fatalismo?",
     "a": "La creencia de que todos los eventos futuros están predeterminados y son inevitables, independientemente de cualquier esfuerzo que hagamos.",
     "keywords": ["fatalismo", "predeterminados", "inevitable", "esfuerzo"],
     "context": "El fatalismo es más fuerte que el determinismo, ya que hace que la intervención humana sea irrelevante para el resultado."},
    {"q": "¿Cuál es la objeción principal del Determinismo contra el Libre Albedrío?",
     "a": "Que nuestras decisiones se pueden explicar completamente por la cadena causal de eventos físicos y biológicos previos.",
     "keywords": ["cadena", "causal", "fisicos", "biologicos", "previos"],
     "context": "La objeción es que la sensación de libertad es solo una percepción subjetiva, no una realidad ontológica."},
    {"q": "¿Cuál es el objetivo principal de la Filosofía Política?",
     "a": "Estudiar la naturaleza, el origen, los límites y la justificación del gobierno, la autoridad, la justicia y la ley.",
     "keywords": ["politica", "naturaleza", "justificacion", "gobierno", "autoridad"],
     "context": "Se enfoca en cómo deberíamos vivir juntos en sociedad y cómo se debe organizar el poder."},
    {"q": "¿Qué teoría explica el origen de la sociedad civil y el Estado como un acuerdo voluntario entre individuos?",
     "a": "La teoría del Contrato Social.",
     "keywords": ["contrato", "social", "acuerdo", "voluntario", "estado"],
     "context": "El Contrato Social legitima la autoridad política en el consentimiento de los gobernados."},
    {"q": "¿Cómo describió Thomas Hobbes el 'estado de naturaleza' (la vida sin gobierno)?",
     "a": "Como una condición miserable, una 'guerra de todos contra todos'.",
     "keywords": ["hobbes", "guerra", "miserable", "todos"],
     "context": "Para Hobbes, la seguridad solo puede obtenerse al ceder los derechos a un poder absoluto (Leviatán)."},
    {"q": "¿Qué derechos consideraba John Locke como inalienables y que el gobierno tiene la obligación de proteger?",
     "a": "La Vida, la Libertad y la Propiedad.",
     "keywords": ["locke", "vida", "libertad", "propiedad", "derechos"],
     "context": "Locke es un pilar del liberalismo, que limita el poder estatal para proteger los derechos individuales."},
    {"q": "¿Qué concepto clave defendió Jean-Jacques Rousseau para justificar la obediencia a la ley en una democracia?",
     "a": "La Voluntad General.",
     "keywords": ["rousseau", "voluntad", "general", "obediencia"],
     "context": "La Voluntad General es la voluntad colectiva que busca el interés común, y a la que todos deben someterse."},
    {"q": "El principio de igualdad en filosofía política se refiere a...",
     "a": "Que todas las personas deben tener el mismo valor y, por lo tanto, el mismo trato, derechos y oportunidades.",
     "keywords": ["igualdad", "mismo", "valor", "trato", "derechos"],
     "context": "La igualdad es fundamental para la justicia; sin embargo, no siempre significa un trato idéntico (equidad)."},
    {"q": "¿Qué es la Justicia Distributiva?",
     "a": "El área de la justicia que se ocupa de la distribución equitativa de los bienes, la riqueza y las oportunidades en la sociedad.",
     "keywords": ["justicia", "distributiva", "distribucion", "riqueza", "oportunidades"],
     "context": "Pregunta cómo deben repartirse los recursos sociales entre los miembros de la comunidad."},
    {"q": "¿Qué pensador argumentó que la justicia requiere que los bienes se distribuyan como si se decidiera desde una 'posición original' bajo un 'velo de ignorancia'?",
     "a": "John Rawls.",
     "keywords": ["rawls", "posicion", "original", "velo", "ignorancia"],
     "context": "El Velo de Ignorancia asegura la imparcialidad en el diseño de las reglas sociales, al no saber qué lugar ocuparás."},
    {"q": "¿Cuál es la forma de gobierno en la que el poder reside en una sola persona (o una familia), generalmente por derecho hereditario?",
     "a": "Monarquía.",
     "keywords": ["monarquia", "sola", "persona", "hereditario"],
     "context": "La Monarquía tradicional justifica su autoridad a menudo por herencia o derecho divino."},
    {"q": "¿Qué se entiende por legitimidad política?",
     "a": "El derecho o justificación de un gobierno para ejercer la autoridad, generalmente a través del consenso o la ley.",
     "keywords": ["legitimidad", "derecho", "justificacion", "consenso"],
     "context": "La legitimidad otorga aceptación y estabilidad al sistema de gobierno."},
    {"q": "¿Qué es la Epistemología?",
     "a": "La rama de la filosofía que estudia el conocimiento: su naturaleza, origen, alcance y justificación.",
     "keywords": ["epistemologia", "conocimiento", "naturaleza", "justificacion"],
     "context": "Es la 'teoría del conocimiento', que pregunta '¿Cómo sabemos lo que sabemos?'."},
    {"q": "¿Cuál es la definición tradicional de conocimiento?",
     "a": "Creencia Verdadera Justificada (CVJ).",
     "keywords": ["creencia", "verdadera", "justificada", "cvj"],
     "context": "Esta definición de Platón ha sido la base para gran parte de la epistemología occidental, aunque enfrenta críticas (problemas de Gettier)."},
    {"q": "La escuela filosófica que enfatiza que el conocimiento se origina principalmente en la razón y la intuición se llama...",
     "a": "Racionalismo (asociado a Descartes).",
     "keywords": ["racionalismo", "razon", "intuicion", "descartes"],
     "context": "El Racionalismo prioriza la lógica y la deducción sobre la experiencia sensorial."},
    {"q": "¿Cuál es la escuela que sostiene que el conocimiento válido proviene fundamentalmente de la experiencia sensorial?",
     "a": "Empirismo (asociado a Locke y Hume).",
     "keywords": ["empirismo", "experiencia", "sensorial", "locke", "hume"],
     "context": "Para el Empirismo, la mente es una 'tabula rasa' al nacer, y todo se aprende de los sentidos."},
    {"q": "¿Cuál es el rol de la justificación en la Epistemología?",
     "a": "Proporcionar las razones, evidencia o el soporte racional para elevar una creencia verdadera al nivel de conocimiento.",
     "keywords": ["justificacion", "razones", "evidencia", "soporte"],
     "context": "La justificación evita que el conocimiento sea simplemente una 'buena suerte' (un acierto casual)."},
    {"q": "¿Qué propuso René Descartes como un método para adquirir conocimiento cierto?",
     "a": "La Duda Metódica (dudar de todo lo que sea posible dudar).",
     "keywords": ["duda", "metodica", "descartes", "dudar"],
     "context": "A través de la duda radical, Descartes llegó a la única certeza: 'Pienso, luego existo' (*Cogito ergo sum*)."},
    {"q": "¿Qué es la verdad desde una perspectiva de correspondencia?",
     "a": "Una creencia es verdadera si corresponde o se ajusta a los hechos de la realidad.",
     "keywords": ["verdad", "corresponde", "ajusta", "hechos", "realidad"],
     "context": "La teoría de la Correspondencia es la noción intuitiva de que la verdad es un 'espejo' del mundo."},
    {"q": "¿Qué es el Escepticismo?",
     "a": "La postura que duda o niega la posibilidad de que los seres humanos adquieran conocimiento cierto y definitivo.",
     "keywords": ["escepticismo", "duda", "niega", "conocimiento", "cierto"],
     "context": "El Escepticismo cuestiona la validez de la justificación y, por tanto, la posibilidad del conocimiento."},
    {"q": "¿Cómo resolvió Immanuel Kant el conflicto entre Racionalismo y Empirismo?",
     "a": "Propuso el Idealismo Trascendental, argumentando que el conocimiento requiere tanto de la experiencia como de las estructuras *a priori* de la razón.",
     "keywords": ["kant", "idealismo", "trascendental", "a priori", "experiencia"],
     "context": "Kant afirmó que no conocemos las 'cosas en sí', sino solo cómo se nos aparecen (fenómenos)."},
    {"q": "¿Qué es el Conocimiento *a priori*?",
     "a": "El conocimiento que se obtiene independientemente de la experiencia (ej. las verdades de la lógica y las matemáticas).",
     "keywords": ["a priori", "independientemente", "experiencia", "logica"],
     "context": "Este conocimiento es necesario y universal; su verdad se conoce solo por la razón."},
    {"q": "¿Cuál es la frase clave de Jean-Paul Sartre que resume la tesis central del Existencialismo?",
     "a": "La existencia precede a la esencia.",
     "keywords": ["sartre", "existencia", "precede", "esencia"],
     "context": "Esta frase invierte la tradición: el ser humano primero existe y luego se define a través de sus actos."},
    {"q": "¿Qué significa 'la existencia precede a la esencia'?",
     "a": "Que el ser humano nace como un lienzo en blanco y se define por sus elecciones y acciones, creando su propia esencia o significado.",
     "keywords": ["elecciones", "acciones", "creando", "esencia", "significado"],
     "context": "Implica que somos radicalmente libres y, por lo tanto, totalmente responsables de lo que somos."},
    {"q": "¿Qué concepto utiliza Albert Camus para describir el conflicto entre la necesidad humana de significado y el silencio del universo?",
     "a": "El Absurdo.",
     "keywords": ["camus", "absurdo", "conflicto", "significado", "silencio"],
     "context": "El Absurdo es la confrontación entre el deseo racional humano y la indiferencia irracional del mundo."},
    {"q": "Según el Existencialismo, ¿por qué surge la Angustia?",
     "a": "Del reconocimiento de la libertad total y la consecuente responsabilidad sobre las elecciones.",
     "keywords": ["angustia", "reconocimiento", "libertad", "responsabilidad"],
     "context": "La angustia es la sensación de peso que se siente al ser consciente de la propia libertad radical."},
    {"q": "¿Qué significa la Mala Fe para Sartre?",
     "a": "Engañarse a uno mismo sobre la propia libertad y responsabilidad, fingiendo ser un objeto o estar determinado.",
     "keywords": ["mala fe", "sartre", "enganarse", "fingiendo", "objeto"],
     "context": "Es el autoengaño de creer que uno está obligado o determinado, evitando así la responsabilidad de ser libre."},
    {"q": "¿Qué filósofo, precursor del existencialismo, argumentó que la existencia se define por la pasión, la fe y la subjetividad, y no por la razón?",
     "a": "Søren Kierkegaard.",
     "keywords": ["kierkegaard", "pasion", "fe", "subjetividad", "precursor"],
     "context": "Kierkegaard enfatizó la angustia de la elección individual en asuntos de fe y vida personal."},
    {"q": "¿Cuál es la actitud que, según Camus, se debe adoptar ante el Absurdo para vivir auténticamente?",
     "a": "La Revuelta y la Conciencia del absurdo.",
     "keywords": ["revuelta", "conciencia", "absurdo", "autenticamente"],
     "context": "La revuelta es el desafío constante contra la falta de sentido, afirmando la vida en medio del absurdo."},
    {"q": "¿Cuál es el tema principal que unifica las ideas de Sartre, Camus y Heidegger?",
     "a": "La Condición Humana y la búsqueda de sentido ante la finitud.",
     "keywords": ["condicion", "humana", "sentido", "finitud"],
     "context": "El Existencialismo se centra en la experiencia del ser humano individual en un mundo sin garantías."},
    {"q": "En el Existencialismo, la libertad se considera...",
     "a": "Absoluta e ineludible; el hombre está 'condenado a ser libre'.",
     "keywords": ["absoluta", "ineludible", "condenado", "libre"],
     "context": "La libertad existencial significa que siempre somos responsables, incluso cuando elegimos no elegir."},
    {"q": "¿Cómo define el Existencialismo la responsabilidad?",
     "a": "La responsabilidad es total: al elegirnos a nosotros mismos, elegimos una imagen de lo que debería ser la humanidad.",
     "keywords": ["responsabilidad", "total", "elegirnos", "imagen", "humanidad"],
     "context": "Sartre dice que nuestras elecciones son un modelo para todos, lo que amplifica la responsabilidad."},
    {"q": "¿Cuál es el objetivo de la Filosofía de la Ciencia?",
     "a": "Analizar los métodos, los fundamentos, la lógica y la validez del conocimiento científico.",
     "keywords": ["ciencia", "metodos", "fundamentos", "logica", "validez"],
     "context": "Pregunta qué hace que una disciplina sea 'científica' y cómo debe proceder la investigación."},
    {"q": "¿Cuál es la diferencia entre una hipótesis y una teoría?",
     "a": "Una Hipótesis es una suposición provisional para ser probada; una Teoría es una explicación bien sustentada y ampliamente probada.",
     "keywords": ["hipotesis", "suposicion", "teoria", "explicacion", "probada"],
     "context": "Una teoría evoluciona a partir de una o más hipótesis que han sido confirmadas repetidamente."},
    {"q": "¿Qué criterio propuso Karl Popper para distinguir la ciencia de la pseudociencia?",
     "a": "El criterio de Falsabilidad (una teoría debe ser potencialmente refutable).",
     "keywords": ["falsabilidad", "popper", "refutable", "distinguir"],
     "context": "Para Popper, una teoría que no se puede probar como falsa no ofrece información genuina sobre el mundo."},
    {"q": "¿Qué es un paradigma científico, según Thomas Kuhn?",
     "a": "Un marco conceptual o conjunto de supuestos y prácticas compartidas por una comunidad científica en un momento dado.",
     "keywords": ["paradigma", "kuhn", "marco", "supuestos", "comunidad"],
     "context": "El paradigma define el tipo de preguntas, problemas y soluciones que son válidos en un campo de la ciencia."},
    {"q": "¿Qué fenómeno, según Kuhn, ocurre cuando un paradigma es reemplazado por otro radicalmente distinto?",
     "a": "Una Revolución Científica.",
     "keywords": ["revolucion", "cientifica", "reemplazado", "distinto"],
     "context": "Una revolución científica implica un cambio completo en la forma en que la comunidad entiende su campo."},
    {"q": "¿Cuál es el papel de la Observación en el método científico?",
     "a": "Proporcionar los datos y hechos empíricos para la formulación de hipótesis y la prueba de teorías.",
     "keywords": ["observacion", "datos", "empiricos", "prueba", "teorias"],
     "context": "La observación es la conexión de la teoría con la realidad del mundo natural."},
    {"q": "¿Qué tipo de razonamiento se utiliza para formular una hipótesis general a partir de observaciones específicas?",
     "a": "Inductivo.",
     "keywords": ["inductivo", "general", "especificas"],
     "context": "El razonamiento inductivo permite ir más allá de los datos observados para postular leyes universales."},
    {"q": "¿Qué es la 'carga teórica' de la observación?",
     "a": "La idea de que lo que observamos siempre está influenciado por nuestros conceptos, teorías o expectativas previas.",
     "keywords": ["carga", "teorica", "influenciado", "expectativas", "conceptos"],
     "context": "Sugiere que la observación 'pura' es imposible, ya que siempre vemos el mundo a través de un marco interpretativo."},
    {"q": "¿Qué significa la Objetividad en la ciencia?",
     "a": "Que las afirmaciones científicas deben estar libres de prejuicios y depender únicamente de la evidencia empírica.",
     "keywords": ["objetividad", "libres", "prejuicios", "evidencia", "empirica"],
     "context": "La objetividad es el ideal de que las conclusiones deben reflejar la realidad, no los sesgos personales del científico."},
    {"q": "¿Cuál es la principal diferencia entre la ciencia pura y la ciencia aplicada?",
     "a": "La ciencia pura busca conocimiento por sí mismo; la aplicada busca resolver problemas prácticos con ese conocimiento.",
     "keywords": ["pura", "aplicada", "conocimiento", "resolver", "problemas"],
     "context": "Ambas son importantes, pero se diferencian en su motivación o propósito final."},
    {"q": "¿Cuál es el principal desafío filosófico del problema Mente-Cuerpo?",
     "a": "Explicar la relación entre los procesos mentales (pensamientos, conciencia) y el cuerpo físico (cerebro).",
     "keywords": ["mente", "cuerpo", "relacion", "cerebro", "conciencia"],
     "context": "El problema se centra en cómo lo inmaterial (la mente) puede interactuar con lo material (el cuerpo)."},
    {"q": "¿Qué postura sostiene que la mente y el cuerpo son dos sustancias radicalmente distintas (una material y una inmaterial)?",
     "a": "Dualismo de Sustancias (propuesto por René Descartes).",
     "keywords": ["dualismo", "sustancias", "descartes", "distintas"],
     "context": "Descartes vio la mente (*res cogitans*) y el cuerpo (*res extensa*) como entidades separadas que interactúan."},
    {"q": "¿Qué sostiene el Monismo Materialista (Fisicalismo)?",
     "a": "Que solo existe la materia física, y la mente es solo un producto o una descripción de los procesos cerebrales.",
     "keywords": ["monismo", "materialista", "fisicalismo", "materia", "cerebrales"],
     "context": "El Materialismo reduce lo mental a lo físico, negando la existencia de una sustancia inmaterial separada."},
    {"q": "¿Qué son las Qualia?",
     "a": "Las cualidades subjetivas y sentidas de las experiencias conscientes (ej. el 'rojo' de ver el color, el 'sabor' del azúcar).",
     "keywords": ["qualia", "subjetivas", "sentidas", "experiencias", "rojo", "sabor"],
     "context": "Son la parte cualitativa de la experiencia; son difíciles de explicar a través de procesos cerebrales puramente físicos."},
    {"q": "¿Qué postula la teoría del Epifenomenalismo?",
     "a": "Que el cerebro causa la mente, pero la mente (la conciencia) no tiene ningún efecto causal sobre el cerebro o el mundo físico.",
     "keywords": ["epifenomenalismo", "causa", "no", "efecto", "conciencia"],
     "context": "La conciencia es vista como un 'humo' o un subproducto del cerebro, sin poder de acción propia."},
    {"q": "¿Qué concepto se refiere al estado de estar despierto y consciente de uno mismo y del entorno?",
     "a": "Conciencia.",
     "keywords": ["conciencia", "despierto", "entorno", "uno mismo"],
     "context": "Es el estado de percatarse y experimentar el mundo de forma subjetiva."},
    {"q": "¿Qué es la Intencionalidad en filosofía de la mente (propuesto por Franz Brentano)?",
     "a": "La característica de los estados mentales de estar dirigidos hacia algo (ej. *creer en algo*, *pensar en algo*).",
     "keywords": ["intencionalidad", "brentano", "dirigidos", "hacia", "algo"],
     "context": "Los estados mentales siempre son 'acerca de' algo, a diferencia de los objetos físicos."},
    {"q": "¿Qué es la Inteligencia Artificial Fuerte?",
     "a": "La idea de que una máquina puede alcanzar una mente y una conciencia humana genuinas.",
     "keywords": ["inteligencia", "artificial", "fuerte", "conciencia", "genuinas"],
     "context": "Se opone a la IA Débil, que solo simula inteligencia sin alcanzar conciencia real."},
    {"q": "¿Cuál es el argumento que utiliza Descartes para probar la existencia de la mente como algo distinto del cuerpo?",
     "a": "El argumento de la Duda (*Pienso, luego existo*): puedo dudar de mi cuerpo, pero no de mi pensamiento.",
     "keywords": ["descartes", "duda", "pienso", "existo", "pensamiento"],
     "context": "La indubitabilidad del pensamiento es la base para postular una sustancia mental separada."},
    {"q": "¿Cómo se llama al proceso de examinar los propios pensamientos y sentimientos?",
     "a": "Introspección.",
     "keywords": ["introspeccion", "examinar", "propios", "sentimientos"],
     "context": "Es la observación de los estados mentales internos por parte del propio sujeto."},
    {"q": "¿Qué rama de la filosofía estudia la naturaleza fundamental de la realidad y el ser?",
     "a": "Metafísica (u Ontología).",
     "keywords": ["metafisica", "ontologia", "naturaleza", "realidad", "ser"],
     "context": "La Metafísica se pregunta '¿Qué es fundamentalmente real?'."},
    {"q": "¿Qué significa que la Realidad es Objetiva?",
     "a": "Que la realidad existe y tiene propiedades independientemente de la conciencia, percepción o creencia de cualquier observador.",
     "keywords": ["objetiva", "independientemente", "conciencia", "observador"],
     "context": "Lo objetivo existe 'ahí fuera', y sus características no cambian por la opinión de nadie."},
    {"q": "¿Qué significa que la Realidad es Subjetiva?",
     "a": "Que la realidad está determinada por la conciencia, la percepción, los sentimientos o los estados mentales del individuo.",
     "keywords": ["subjetiva", "determinada", "conciencia", "percepcion", "individual"],
     "context": "Lo subjetivo es relativo a la experiencia personal y varía de una persona a otra."},
    {"q": "¿Qué teoría sobre el tiempo afirma que solo el Presente es real?",
     "a": "Presentismo.",
     "keywords": ["presentismo", "presente", "solo", "real"],
     "context": "El Presentismo sostiene que el pasado y el futuro no existen en un sentido literal."},
    {"q": "¿Qué teoría sobre el tiempo (influenciada por la Relatividad de Einstein) afirma que el Pasado, el Presente y el Futuro existen simultáneamente y son igualmente reales?",
     "a": "Eternalismo (o Teoría del Bloque).",
     "keywords": ["eternalismo", "bloque", "simultaneamente", "igualmente"],
     "context": "El Eternalismo trata el tiempo como una dimensión espacial, donde todos los momentos están fijos y son existentes."},
    {"q": "¿Qué es una Sustancia en la metafísica clásica?",
     "a": "Aquello que existe por sí mismo y no depende de otra cosa para su existencia.",
     "keywords": ["sustancia", "existe", "si mismo", "depende", "otra cosa"],
     "context": "Es el sustrato fundamental que subyace a las propiedades y los accidentes."},
    {"q": "¿Qué filósofo resumió el Idealismo al afirmar 'Ser es ser percibido' (*Esse est percipi*)?",
     "a": "George Berkeley.",
     "keywords": ["berkeley", "ser", "percibido", "esse", "percipi"],
     "context": "Berkeley argumentó que los objetos materiales solo existen como ideas en la mente de un perceptor (o en la mente de Dios)."},
    {"q": "¿Cuál es el principal argumento del Idealismo?",
     "a": "Que la realidad fundamental es mental, conciencia o ideas, y que el mundo material depende de la mente.",
     "keywords": ["idealismo", "mental", "conciencia", "ideas", "depende"],
     "context": "El Idealismo niega que la materia sea una sustancia independiente de la conciencia."},
    {"q": "¿Qué es el Mundo Fenoménico para Kant?",
     "a": "El mundo tal como lo experimentamos, filtrado por nuestras estructuras cognitivas (opuesto al *noúmeno* o cosa en sí).",
     "keywords": ["fenomenico", "kant", "experimentamos", "estructuras", "cognitivas"],
     "context": "Es el mundo de la experiencia posible, ordenado por las categorías de nuestro entendimiento."},
    {"q": "En física y filosofía, ¿cómo se define el Tiempo?",
     "a": "La progresión continua e irreversible de la existencia y los eventos del pasado hacia el presente y el futuro.",
     "keywords": ["tiempo", "progresion", "irreversible", "existencia", "eventos"],
     "context": "El tiempo se entiende como la medida del cambio y el orden de los sucesos."},
    {"q": "¿Qué escuela ética sostiene que la moralidad de un acto depende únicamente de sus consecuencias?",
     "a": "Consecuencialismo",
     "keywords": ["consecuencialismo", "consecuencias", "resultados"],
     "context": "Esta teoría se contrapone a las éticas deontológicas, que se centran en el deber."},
    {"q": "¿Qué principio ético se asocia con el filósofo Immanuel Kant?",
     "a": "El Imperativo Categórico.",
     "keywords": ["imperativo", "categorico", "kant"],
     "context": "El Imperativo Categórico es una regla universal para la acción, que ordena hacer el bien por el deber mismo."},
    {"q": "¿La ética de la virtud se centra en las reglas, las consecuencias o el carácter?",
     "a": "El Carácter (la formación de la virtud).",
     "keywords": ["caracter", "virtud", "formacion", "aristoteles"],
     "context": "Busca cultivar hábitos buenos en lugar de simplemente seguir reglas o calcular resultados."},
    {"q": "¿Qué es el Nihilismo Moral?",
     "a": "La creencia de que no existen valores morales objetivos o intrínsecos.",
     "keywords": ["nihilismo", "moral", "objetivos", "intrinsecos"],
     "context": "Postula que todas las distinciones morales son, en última instancia, sin sentido o ilusorias."},
    {"q": "¿Qué teoría ética sostiene que el placer es el bien supremo y la meta de la vida?",
     "a": "Hedonismo.",
     "keywords": ["hedonismo", "placer", "bien", "supremo"],
     "context": "Filósofos como Epicuro defendieron versiones más sofisticadas del Hedonismo."},
    {"q": "¿Qué falacia comete alguien que apela a la lástima o emoción en lugar de a la razón?",
     "a": "Ad Misericordiam.",
     "keywords": ["ad misericordiam", "lastima", "emocion"],
     "context": "Es una falacia de relevancia que intenta manipular la respuesta emocional del oyente."},
    {"q": "¿Qué es un Silogismo?",
     "a": "Un argumento deductivo compuesto por dos premisas y una conclusión.",
     "keywords": ["silogismo", "deductivo", "dos", "premisas"],
     "context": "Es la forma más básica y estudiada del razonamiento deductivo (ej. 'Todos los hombres son mortales...')."},
    {"q": "La falacia que asume que una cosa es cierta porque la mayoría de la gente cree que es cierta se llama...",
     "a": "Ad Populum.",
     "keywords": ["ad populum", "mayoria", "gente", "cree"],
     "context": "La popularidad de una idea no es evidencia de su verdad o validez lógica."},
    {"q": "¿Qué ley lógica establece que toda cosa es idéntica a sí misma?",
     "a": "Principio de Identidad.",
     "keywords": ["identidad", "ley", "logica", "misma"],
     "context": "Es el principio fundamental que establece que A es A."},
    {"q": "¿Qué tipo de razonamiento se utiliza para descartar hipótesis cuando se encuentra un contraejemplo?",
     "a": "Deductivo (mediante el Modus Tollens).",
     "keywords": ["modus tollens", "deductivo", "contraejemplo", "descartar"],
     "context": "Si se niega el consecuente, se puede negar el antecedente de forma lógicamente válida."},
    {"q": "¿Cuál es la objeción principal a la teoría de la identidad basada en la continuidad del cuerpo?",
     "a": "El cuerpo cambia constantemente a nivel celular, y su identidad numérica es difícil de establecer.",
     "keywords": ["cuerpo", "cambia", "celular", "dificil"],
     "context": "Los procesos biológicos constantes desafían la idea de un cuerpo inmutable a lo largo de la vida."},
    {"q": "¿Quién introdujo el concepto de Intersubjetividad para entender la identidad?",
     "a": "Pensadores fenomenológicos (como Husserl o Sartre).",
     "keywords": ["intersubjetividad", "fenomenologicos", "husserl", "sartre"],
     "context": "La identidad se construye no solo individualmente, sino a través del reconocimiento de otros 'Yoes'."},
    {"q": "¿Qué postula el Existencialismo sobre la identidad antes de nacer?",
     "a": "Que el ser humano no tiene una esencia o naturaleza predefinida antes de su existencia.",
     "keywords": ["esencia", "predefinida", "existencialismo", "nacer"],
     "context": "El Existencialismo rechaza que haya un 'diseño' humano inherente, a diferencia de un utensilio."},
    {"q": "¿Qué es la 'Identidad Narrativa' (Paul Ricoeur)?",
     "a": "La idea de que construimos el Yo a través de la historia o relato que contamos sobre nosotros mismos.",
     "keywords": ["narrativa", "ricoeur", "historia", "relato"],
     "context": "Sugiere que nuestra identidad es dinámica y se reescribe constantemente con cada experiencia."},
    {"q": "¿Qué es el Dualismo Interaccionista?",
     "a": "La postura de Descartes que afirma que la mente y el cuerpo son distintos, pero interactúan en un punto (la glándula pineal).",
     "keywords": ["dualismo", "interaccionista", "glandula", "pineal", "interactuan"],
     "context": "Esta teoría enfrenta el problema de cómo dos sustancias de naturaleza diferente pueden influirse causalmente."},
    {"q": "¿Qué implica el Libertarianismo (posición sobre el libre albedrío)?",
     "a": "El Libre Albedrío es real y, por lo tanto, el Determinismo es falso.",
     "keywords": ["libertarianismo", "real", "falso", "determinismo"],
     "context": "Es una forma de Incompatibilismo que prioriza la libertad de elección del agente."},
    {"q": "¿Cómo se llama la posición que afirma que el Universo y el futuro están predeterminados por Dios?",
     "a": "Predeterminación o Determinismo Teológico.",
     "keywords": ["predeterminacion", "teologico", "dios", "futuro"],
     "context": "Esta postura plantea un conflicto con el concepto de la bondad de Dios y el castigo por el pecado."},
    {"q": "¿Qué significa que un acto es 'voluntario' en el contexto del libre albedrío?",
     "a": "Que el acto fue causado por la voluntad, deseo o razón del agente, sin coerción externa.",
     "keywords": ["voluntario", "voluntad", "agente", "coercion", "externa"],
     "context": "La acción voluntaria es el requisito mínimo para que se pueda hablar de responsabilidad."},
    {"q": "¿Qué objeción plantea la física cuántica al Determinismo clásico?",
     "a": "La existencia de eventos subatómicos aleatorios (Indeterminismo cuántico).",
     "keywords": ["cuantica", "subatomicos", "aleatorios", "indeterminismo"],
     "context": "Algunos filósofos intentan usar este azar cuántico como base física para el libre albedrío."},
    {"q": "¿Qué diferencia existe entre un gobierno oligárquico y uno democrático?",
     "a": "La Oligarquía es el gobierno de unos pocos ricos; la Democracia es el gobierno del pueblo o la mayoría.",
     "keywords": ["oligarquia", "pocos", "ricos", "democracia", "pueblo"],
     "context": "La diferencia clave es quién ejerce el poder soberano en el Estado."},
    {"q": "¿Qué es el 'Estado de Derecho'?",
     "a": "El principio de que nadie está por encima de la ley, ni siquiera el gobierno, y todos están sujetos a normas claras.",
     "keywords": ["estado", "derecho", "nadie", "ley", "normas"],
     "context": "Es esencial para proteger a los ciudadanos de la arbitrariedad y el abuso de poder."},
    {"q": "¿Qué es la 'Separación de Poderes' y quién la popularizó?",
     "a": "Dividir el gobierno en poderes Ejecutivo, Legislativo y Judicial; popularizada por Montesquieu.",
     "keywords": ["separacion", "poderes", "ejecutivo", "legislativo", "montesquieu"],
     "context": "Busca limitar el poder impidiendo que una sola rama tenga control absoluto."},
    {"q": "¿Cuál es la crítica principal de Karl Marx a la democracia liberal?",
     "a": "Que es una 'superestructura' que sirve a los intereses de la clase dominante (burguesía) y no a los del pueblo.",
     "keywords": ["marx", "critica", "burguesia", "clase", "dominante"],
     "context": "Marx argumentó que la igualdad política es ilusoria sin igualdad económica."},
    {"q": "¿Qué diferencia existe entre libertad negativa y libertad positiva?",
     "a": "La negativa es 'libertad de' interferencia externa; la positiva es 'libertad para' actuar y lograr metas.",
     "keywords": ["negativa", "interferencia", "positiva", "actuar", "lograr"],
     "context": "La libertad negativa requiere menos Estado; la positiva puede requerir más intervención para crear oportunidades."},
    {"q": "¿Qué son los 'Problemas de Gettier' en Epistemología?",
     "a": "Casos en los que una persona tiene una Creencia Verdadera Justificada, pero no parece tener conocimiento, lo que desafía la definición tradicional.",
     "keywords": ["gettier", "casos", "creencia", "justificada", "desafia"],
     "context": "Estos problemas muestran que la definición CVJ no es suficiente por sí sola para el conocimiento."},
    {"q": "¿Qué sostiene la teoría Fundacionalista sobre la justificación?",
     "a": "Que el conocimiento se construye sobre un conjunto de creencias básicas, ciertas e incuestionables (fundamentos).",
     "keywords": ["fundacionalista", "creencias", "basicas", "fundamentos"],
     "context": "Busca detener la regresión infinita de la justificación encontrando un punto de apoyo firme."},
    {"q": "¿Qué sostiene la teoría Coherentista sobre la justificación?",
     "a": "Que una creencia está justificada si encaja lógicamente con un gran conjunto de otras creencias que posee el sujeto (coherencia).",
     "keywords": ["coherentista", "encaja", "logicamente", "conjunto", "creencias"],
     "context": "Se asemeja a una red o un rompecabezas: la justificación viene de la relación mutua, no de un fundamento único."},
    {"q": "¿Cuál es el postulado central del Racionalismo en cuanto al origen de las ideas?",
     "a": "La existencia de ideas o principios innatos en la mente (ej. la idea de Dios, las verdades matemáticas).",
     "keywords": ["innatas", "principios", "racionalismo", "mente"],
     "context": "Niegan que la mente sea una 'tabula rasa' y afirman que el conocimiento esencial viene de dentro."},
    {"q": "¿Qué es una verdad 'a posteriori'?",
     "a": "Una verdad cuyo conocimiento requiere necesariamente de la experiencia o la observación (ej. 'El cielo es azul').",
     "keywords": ["a posteriori", "experiencia", "observacion", "necesariamente"],
     "context": "Son verdades contingentes que se descubren mediante la investigación empírica."},
    {"q": "¿Cómo se llama la sensación de vacío y falta de propósito asociada al Existencialismo?",
     "a": "Nausea (náusea) o Abandono.",
     "keywords": ["nausea", "abandono", "vacio", "proposito"],
     "context": "La Náusea (Sartre) es el sentimiento de contingencia ante la falta de significado preordenado."},
    {"q": "¿Qué significa el concepto de 'El Otro' en el Existencialismo de Sartre?",
     "a": "Cualquier otra persona cuya mirada nos objetiva, definiendo quiénes somos y limitando nuestra libertad.",
     "keywords": ["el otro", "mirada", "objetiva", "limita", "libertad"],
     "context": "La existencia de El Otro crea el conflicto de la intersubjetividad y la vergüenza."},
    {"q": "¿Cuál es la 'condena' del hombre en la filosofía existencial?",
     "a": "Estar condenado a ser libre, sin excusas ni justificaciones divinas o naturales para sus actos.",
     "keywords": ["condena", "libre", "sin excusas", "justificaciones"],
     "context": "La falta de esencia predefinida nos obliga a inventarnos a cada paso."},
    {"q": "¿Qué pensador existencialista enfocó su obra en el concepto de la autenticidad y el *Dasein* (ser-ahí)?",
     "a": "Martin Heidegger.",
     "keywords": ["heidegger", "dasein", "ser-ahi", "autenticidad"],
     "context": "El *Dasein* es el ser que está arrojado al mundo y se enfrenta a su propia finitud (muerte)."},
    {"q": "¿Qué significa el 'Salto de Fe' para Kierkegaard?",
     "a": "La decisión irracional y profundamente personal de abrazar la fe a pesar del riesgo y el Absurdo.",
     "keywords": ["salto", "fe", "kierkegaard", "irracional", "abrazar"],
     "context": "Implica suspender la ética y la razón en favor de una relación individual con lo divino."},
    {"q": "¿Qué son las 'Ciencias Normales' según Thomas Kuhn?",
     "a": "La actividad científica que se desarrolla dentro de un paradigma establecido, resolviendo 'puzzles' en lugar de cuestionar los fundamentos.",
     "keywords": ["normales", "kuhn", "establecido", "puzzles", "fundamentos"],
     "context": "Es la ciencia que se hace la mayor parte del tiempo, basada en el consenso de un marco teórico."},
    {"q": "¿Qué son las Anomalías en el contexto del cambio de paradigma?",
     "a": "Observaciones que contradicen o no pueden explicarse con el paradigma científico actualmente aceptado.",
     "keywords": ["anomalias", "observaciones", "contradicen", "paradigma", "aceptado"],
     "context": "Una acumulación de anomalías puede conducir a una crisis y, eventualmente, a una revolución científica."},
    {"q": "¿Qué es el 'Inconmensurabilidad' (Kuhn/Feyerabend)?",
     "a": "La idea de que los conceptos y términos de dos paradigmas o teorías diferentes son tan distintos que no se pueden comparar directamente o traducir entre sí.",
     "keywords": ["inconmensurabilidad", "conceptos", "terminos", "comparar", "traducir"],
     "context": "Sugiere que un científico de un paradigma no ve el mundo de la misma forma que otro de un paradigma distinto."},
    {"q": "¿Qué es la 'Navaja de Ockham'?",
     "a": "Un principio que aconseja elegir la explicación más simple o la que requiere menos supuestos.",
     "keywords": ["navaja", "ockham", "simple", "menos", "supuestos"],
     "context": "Es una regla heurística utilizada en la ciencia para favorecer la parsimonia teórica."},
    {"q": "¿Qué es una ley científica?",
     "a": "Una descripción de un fenómeno natural que ha sido repetidamente probada y se considera universalmente verdadera.",
     "keywords": ["ley", "cientifica", "descripcion", "probada", "universalmente"],
     "context": "Las leyes describen 'cómo' funciona la naturaleza, mientras que las teorías explican 'por qué'."},
    {"q": "¿Cuál es el nombre del argumento que usa el científico Fred para demostrar que la conciencia no se reduce a procesos físicos?",
     "a": "El Argumento del Conocimiento (o 'Mary's Room').",
     "keywords": ["argumento", "conocimiento", "mary", "fred", "no", "reduce"],
     "context": "Señala que saber todos los hechos físicos no es lo mismo que tener la experiencia consciente (qualia)."},
    {"q": "¿Qué es el Conductismo Filosófico sobre la mente?",
     "a": "La idea de que los estados mentales son simplemente descripciones de patrones de comportamiento y disposiciones a actuar.",
     "keywords": ["conductismo", "patrones", "comportamiento", "disposiciones"],
     "context": "Intenta resolver el problema mente-cuerpo eliminando la necesidad de una sustancia mental interna."},
    {"q": "¿Qué teoría sostiene que la mente es como un *software* que se ejecuta en el *hardware* del cerebro, y podría ejecutarse en otro hardware?",
     "a": "Funcionalismo.",
     "keywords": ["funcionalismo", "software", "hardware", "ejecuta"],
     "context": "Se centra en lo que la mente hace (su función), no en el material del que está hecha."},
    {"q": "¿Qué es la 'Causalidad Mental'?",
     "a": "El problema de explicar cómo los estados mentales (pensamientos) pueden causar o influir en las acciones físicas (movimientos corporales).",
     "keywords": ["causalidad", "mental", "estados", "influir", "acciones"],
     "context": "Es el desafío central para el Dualismo y el Epifenomenalismo."},
    {"q": "¿Qué significa que la conciencia es 'subjetiva'?",
     "a": "Que solo el sujeto que experimenta puede acceder a sus propios estados mentales de manera directa e inmediata.",
     "keywords": ["subjetiva", "sujeto", "acceder", "directa", "inmediata"],
     "context": "El acceso a la conciencia es de 'primera persona', lo que la diferencia de los objetos físicos de 'tercera persona'."},
    {"q": "¿Qué es el 'Presente Expandido' o Presente 'Grueso'?",
     "a": "La idea de que la experiencia consciente del presente no es un punto sin duración, sino que abarca un lapso corto de pasado y futuro.",
     "keywords": ["presente", "expandido", "grueso", "lapso", "duracion"],
     "context": "Se utiliza para explicar cómo experimentamos la continuidad del movimiento o el tiempo."},
    {"q": "¿Cuál es la objeción principal del Eternalismo al Presentismo?",
     "a": "Que el Presentismo es incompatible con la Teoría de la Relatividad Especial de Einstein, que no define un 'ahora' absoluto.",
     "keywords": ["eternalismo", "relatividad", "einstein", "incompatible", "absoluto"],
     "context": "La física moderna desafía la noción intuitiva de un presente universal."},
    {"q": "¿Qué es el Idealismo de George Berkeley?",
     "a": "Idealismo Subjetivo: solo existen las ideas en la mente del perceptor, negando la existencia de la materia si no es percibida.",
     "keywords": ["idealismo", "berkeley", "subjetivo", "ideas", "materia"],
     "context": "Su lema 'Ser es ser percibido' resume su tesis de que el mundo es mental."},
    {"q": "¿Qué es la diferencia entre el *Noúmeno* y el *Fenómeno* para Kant?",
     "a": "El *Fenómeno* es la realidad experimentada; el *Noúmeno* es la realidad subyacente o 'cosa en sí', incognoscible.",
     "keywords": ["noumeno", "fenomeno", "kant", "incognoscible", "subyacente"],
     "context": "Kant traza una línea divisoria estricta sobre lo que podemos conocer (fenómeno) y lo que no (noúmeno)."},
    {"q": "¿Qué afirma la teoría del 'Realismo Ingenuo'?",
     "a": "Que percibimos el mundo directamente, tal como es, sin que la mente altere o filtre la realidad.",
     "keywords": ["realismo", "ingenuo", "directamente", "filtre", "altere"],
     "context": "Es la creencia intuitiva de que nuestros sentidos nos dan acceso directo y verídico al mundo."},
    {"q": "¿Qué es la 'Causalidad' en Metafísica?",
     "a": "La relación necesaria entre un evento (la causa) y un segundo evento (el efecto), donde la causa produce o determina el efecto.",
     "keywords": ["causalidad", "relacion", "necesaria", "produce", "determina"],
     "context": "Es un concepto clave para entender el Determinismo y las leyes de la naturaleza."},
    {"q": "¿Qué filósofo criticó la idea de la 'Causalidad' argumentando que solo observamos la 'conjunción constante' de eventos?",
     "a": "David Hume.",
     "keywords": ["hume", "critico", "causalidad", "conjuncion", "constante"],
     "context": "Hume puso en duda si la conexión entre causa y efecto es necesaria o simplemente un hábito mental."},
]
 
# This function checks if the user's answer is close to the
correct one using a similarity ratio
def
is_correct(user_answer, keywords):
    # Sanitize user input by removing
punctuation, extra spaces, and converting to lowercase
    user_answer = re.sub(r'[^\w\s]', '',
user_answer).lower().strip()
    
    # Check for direct keyword matches
    for keyword in keywords:
        # Use re.search for more flexible matching
(e.g., matching a keyword within a longer answer)
        if re.search(r'\b' + re.escape(keyword) +
r'\b', user_answer):
            return True
 
        # Also check if the user's answer
contains the keyword without strict word boundaries
        if keyword in user_answer:
            return True
 
    # If no direct match, calculate similarity
ratio
    # (Note: The original similarity logic is kept as
a fallback, but keyword matching is prioritized for accuracy)
    for keyword in keywords:
        # Check for individual words in the
user's answer
        for user_word in user_answer.split():
            # A similarity ratio of 0.85 or
higher is considered a match
            if SequenceMatcher(None, user_word,
keyword).ratio() > 0.85:
                return True
    
    return False
 
# Initialize
session state for the quiz
if
"score" not in st.session_state:
    st.session_state.score = 0
if
"current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if
"question_list" not in st.session_state:
    st.session_state.question_list = []
if
"name_set" not in st.session_state:
    st.session_state.name_set = False
if
"feedback" not in st.session_state:
    st.session_state.feedback = None
if
"user_answer" not in st.session_state:
    st.session_state.user_answer = ""
if
"quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
 
# This function resets the quiz state
def reset_quiz():
    st.session_state.score = 0
    st.session_state.current_question_index = 0
    # Selecciona 20 preguntas al azar de un
banco de 100
    num_questions = min(20, len(questions))
    st.session_state.question_list = random.sample(questions, num_questions)
    st.session_state.feedback = None
    st.session_state.user_answer = ""
    st.session_state.quiz_started = True
    st.rerun()
 
# Display the main title
st.title("📝 Práctica Concurso - Filosofía
para Mentes Brillantes")
 
# Get user's name
if not
st.session_state.name_set:
    # Personalizamos el input con el nombre
de la estudiante como referencia, aunque el código lo pida de nuevo.
    name = st.text_input("¡Hola! Para
empezar, por favor, dime tu nombre.")
    if name:
        st.session_state.name = name
        st.session_state.name_set = True
        st.session_state.quiz_started =
False  # Reset quiz_started after setting
the name
        st.rerun()
else:
    name = st.session_state.name
    # El mensaje de bienvenida ahora es más
relevante.
    st.subheader(f"¡Hola {name}! Empecemos
con la preparación en Filosofía. ¡Ánimo, Analía! 📚")
 
    if not st.session_state.quiz_started:
        st.info(f"Se seleccionarán
**20 preguntas al azar** de un total de 100 en cada sesión de práctica.")
        if st.button("Iniciar
Práctica"):
           reset_quiz()
    else:
        # Check if the
quiz is finished
       total_questions = len(st.session_state.question_list)
        if st.session_state.current_question_index >=
total_questions:
            st.success(f"🎉
¡Has completado la ronda! Tu puntaje es:
{st.session_state.score}/{total_questions}")
            if
st.button("Empezar de Nuevo"):
                st.session_state.quiz_started = False
                st.rerun()
        else:
            # Display the current question
            current_question =
st.session_state.question_list[st.session_state.current_question_index]
 
            st.write(f"**Pregunta
{st.session_state.current_question_index + 1}/{total_questions}:**
{current_question['q']}")
            
            # Text input for the user's answer
            # Use a unique key based on the
index to ensure proper reset on "Siguiente"
            user_answer =
st.text_input("Tu respuesta:",
value=st.session_state.get("user_answer", ""),
key=f"answer_input_{st.session_state.current_question_index}")
 
            # Handle the "Responder" button
            if st.button("Responder",
key=f"btn_respond_{st.session_state.current_question_index}"):
                if user_answer.strip() ==
"":
                    st.warning("Por favor,
ingresa una respuesta antes de continuar.")
                else:
                    if is_correct(user_answer,
current_question['keywords']):
                        st.session_state.score
+= 1
                       st.session_state.feedback = "correct"
                    else:
                       st.session_state.feedback = "incorrect"
                    
                   st.session_state.user_answer = user_answer
                    st.rerun()
 
            # Display
feedback and the "Siguiente Pregunta" button
            if
st.session_state.get("feedback"):
                if st.session_state.feedback ==
"correct":
                    st.success("✅¡Correcto! ¡Sigue
así, Analía!")
                else:
                   st.error("❌ Incorrecto.
¡Pero no te rindas!")
                   st.write(f"La respuesta correcta era:
**{current_question['a']}**")
                   st.info(f"📖 **Para profundizar,
puedes revisar:** {current_question['context']}")
 
                if
st.button("Siguiente Pregunta",
key=f"btn_next_{st.session_state.current_question_index}"):
                    st.session_state.current_question_index +=
1
                    st.session_state.feedback =
None
                    # Clear the user answer
state for the next question
                   st.session_state.user_answer = "" 
                    st.rerun()
 
            st.write("---")
            st.write(f"### Puntaje actual:
{st.session_state.score}/{st.session_state.current_question_index}")
