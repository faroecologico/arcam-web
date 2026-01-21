import requests
import json
import time
import os
from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()

# --- TUS CREDENCIALES ---
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET") 

# ==============================================================================
# 🧠 MAPA DE CATEGORÍAS (Generado por IA para Arcam)
# ==============================================================================
MAPA_CATEGORIAS = {
    # --- Papelería y Oficina ---
    "LIBR.": "Papelería y Oficina",
    "BOLIGRAFO": "Papelería y Oficina",
    "PLUMON": "Papelería y Oficina",
    "CUADERNO": "Papelería y Oficina",
    "CARPETA": "Papelería y Oficina",
    "ARCHIVADOR": "Papelería y Oficina",
    "CORCHETERA": "Papelería y Oficina",
    "CORCHETES": "Papelería y Oficina",
    "POST IT": "Papelería y Oficina",
    "PIZARRA": "Papelería y Oficina",
    "BARRA ADHESIVA": "Papelería y Oficina",
    "PEGAMENTO EN BARRA": "Papelería y Oficina",

    # --- Cerraduras digitales / Seguridad electrónica ---
    "HUB POLI HOME": "Cerraduras Digitales",
    "CERRADURA DIGITAL": "Cerraduras Digitales",
    "CERRADURA SMART": "Cerraduras Digitales",
    "POLI HOME": "Cerraduras Digitales",
    "CAMARA SEGURIDAD": "Seguridad Electrónica",
    "CAMARA SEG.": "Seguridad Electrónica",
    "CÁMARA SEG.": "Seguridad Electrónica",
    "EZVIZ": "Seguridad Electrónica",

    # --- Portones y Automatización ---
    "MOTOR PARA PORTON": "Portones y Automatización",
    "CONTROL REMOTO PARA PORTON": "Portones y Automatización",
    "CONTROL REMOTO PORTON": "Portones y Automatización",
    "FOTOCELDA": "Portones y Automatización",
    "CREMALLERA": "Portones y Automatización",
    "RUEDA PARA PORTON": "Portones y Automatización",
    "GUIA PARA PORTON": "Portones y Automatización",
    "CARRO PARA PORTON": "Portones y Automatización",

    # --- Primeros Auxilios ---
    "INSUMOS BOTIQUIN": "Primeros Auxilios",
    "BOTIQUIN": "Primeros Auxilios",
    "CAMILLA": "Primeros Auxilios",
    "ARAÑA CAMILLA": "Primeros Auxilios",
    "PULPO ARAÑA CAMILLA": "Primeros Auxilios",
    "FERULA": "Primeros Auxilios",
    "COLLAR - CERVICAL": "Primeros Auxilios",
    "COLLAR CERVICAL": "Primeros Auxilios",
    "VENDA": "Primeros Auxilios",
    "GASA": "Primeros Auxilios",

    # --- Extintores / Contra incendios ---
    "GABINETE EXTINTOR": "Extintores y Contra Incendios",
    "GABINETE - EXTINTOR": "Extintores y Contra Incendios",
    "SOPORTE EXTINTOR": "Extintores y Contra Incendios",
    "EXTINTOR": "Extintores y Contra Incendios",

    # --- Señalización y Seguridad vial ---
    "CINTA - PELIGRO": "Señalización y Seguridad Vial",
    "CINTA DEMARCACION": "Señalización y Seguridad Vial",
    "CADENA PLASTICA": "Señalización y Seguridad Vial",
    "BALIZA": "Señalización y Seguridad Vial",
    "BANDERIN": "Señalización y Seguridad Vial",
    "BANDERINES": "Señalización y Seguridad Vial",
    "CONO SEGURIDAD": "Señalización y Seguridad Vial",
    "TOPE ESTACIONAMIENTO": "Señalización y Seguridad Vial",
    "ESPEJO PANORAMICO": "Señalización y Seguridad Vial",
    "ESPEJO CONVEXO": "Señalización y Seguridad Vial",
    "BOCINA EMERGENCIA": "Señalización y Seguridad Vial",

    # --- Protección contra caídas ---
    "ARNES - PARACAIDISTA": "Protección contra Caídas",
    "ARNES PARACAIDISTA": "Protección contra Caídas",
    "ARNÉS PARACAIDISTA": "Protección contra Caídas",
    "CABO - DE VIDA": "Protección contra Caídas",
    "CABO DE VIDA": "Protección contra Caídas",
    "AMORTIGUADOR - DE CAIDA": "Protección contra Caídas",
    "AMORTIGUADOR DE CAIDA": "Protección contra Caídas",
    "AMORTIGUADOR - DE CAÍDA": "Protección contra Caídas",
    "AMORTIGUADOR DE CAÍDA": "Protección contra Caídas",
    "LINEA DE VIDA": "Protección contra Caídas",
    "LÍNEA DE VIDA": "Protección contra Caídas",
    "MOSQUETON": "Protección contra Caídas",
    "MOSQUETÓN": "Protección contra Caídas",
    "ESLINGA DE POSICIONAMIENTO": "Protección contra Caídas",
    "CINTURON LINIERO": "Protección contra Caídas",

    # --- Izaje / Amarre de carga ---
    "CINTA TRINQUETE": "Izaje y Sujeción de Carga",
    "TRINQUETE": "Izaje y Sujeción de Carga",
    "TENSOR": "Izaje y Sujeción de Carga",
    "ESTROBO": "Izaje y Sujeción de Carga",
    "CABLE DE ACERO": "Izaje y Sujeción de Carga",
    "GRILLETE": "Izaje y Sujeción de Carga",
    "ESLINGA": "Izaje y Sujeción de Carga",

    # --- EPP ---
    "ADAPTADOR - PARA CASCO": "EPP - Protección de Cabeza",
    "ADAPTADOR PARA CASCO": "EPP - Protección de Cabeza",
    "SOTOCASCO": "EPP - Protección de Cabeza",
    "BARBOQUEJO": "EPP - Protección de Cabeza",
    "BARBIQUEJO": "EPP - Protección de Cabeza",
    "CASCO": "EPP - Protección de Cabeza",
    "ANTIPARRA": "EPP - Protección Ocular",
    "LENTE": "EPP - Protección Ocular",
    "MASCARA SOLDAR": "EPP - Protección Facial",
    "MASCARA SOLDADOR": "EPP - Protección Facial",
    "MASCARA FOTOSENSIBLE": "EPP - Protección Facial",
    "CARETA": "EPP - Protección Facial",
    "PROTECTOR FACIAL": "EPP - Protección Facial",
    "VISOR POLICARBONATO": "EPP - Protección Facial",
    "VISOR": "EPP - Protección Facial",
    "RETENEDOR PARA FILTRO": "EPP - Filtros Respiratorios",
    "PREFILTRO": "EPP - Filtros Respiratorios",
    "FILTRO 3M": "EPP - Filtros Respiratorios",
    "FILTRO ERGONIC": "EPP - Filtros Respiratorios",
    "FILTRO MASPROT": "EPP - Filtros Respiratorios",
    "RESPIRADOR": "EPP - Protección Respiratoria",
    "MASCARILLA": "EPP - Protección Respiratoria",
    "OREJERA": "EPP - Protección Auditiva",
    "FONO": "EPP - Protección Auditiva",
    "TAPON": "EPP - Protección Auditiva",
    "TAPÓN": "EPP - Protección Auditiva",
    "GUANTE NITRILO": "EPP - Protección de Manos - Desechables",
    "GUANTE LATEX": "EPP - Protección de Manos - Desechables",
    "GUANTE VINILO": "EPP - Protección de Manos - Desechables",
    "GUANTE DESECHABLE": "EPP - Protección de Manos - Desechables",
    "GUANTE DESCARNE": "EPP - Protección de Manos - Cuero",
    "GUANTE VAQUETA": "EPP - Protección de Manos - Cuero",
    "GUANTE CUERO": "EPP - Protección de Manos - Cuero",
    "GUANTE ANTICORTE": "EPP - Protección de Manos - Anticorte",
    "GUANTE DIELECTRICO": "EPP - Protección de Manos - Dieléctrico",
    "GUANTE": "EPP - Protección de Manos",
    "MANGUILLAS": "EPP - Protección de Brazos",
    "RODILLERA": "EPP - Protección de Rodillas",
    "FAJA LUMBAR": "EPP - Ergonomía y Soporte Lumbar",
    "FAJA": "EPP - Ergonomía y Soporte Lumbar",

    # --- Calzado / Vestuario ---
    "BOTA PESCADORA": "Calzado - Botas de Agua y Pesca",
    "BOTA DE AGUA": "Calzado - Botas de Agua y Pesca",
    "BOTA AGUA": "Calzado - Botas de Agua y Pesca",
    "PROTECTOR METATARSO": "Accesorios de Calzado",
    "METATARSO": "Accesorios de Calzado",
    "PLANTILLA": "Accesorios de Calzado",
    "CORDON": "Accesorios de Calzado",
    "CUBRECALZADO": "Ropa Desechable",
    "BOTÍN": "Calzado de Seguridad",
    "BOTIN": "Calzado de Seguridad",
    "BOTA": "Calzado de Seguridad",
    "ZAPATO": "Calzado de Seguridad",
    "ZAPATILLA": "Calzado de Seguridad",
    "CHALECO REFLECTANTE": "Ropa de Alta Visibilidad",
    "REFLECTANTE": "Ropa de Alta Visibilidad",
    "ALTA VISIBILIDAD": "Ropa de Alta Visibilidad",
    "CINTA REFLECTIVA": "Ropa de Alta Visibilidad",
    "TRAJE DE AGUA": "Ropa Impermeable",
    "IMPERMEABLE": "Ropa Impermeable",
    "PRIMERA CAPA": "Ropa Térmica",
    "PIJAMA": "Ropa Térmica",
    "TÉRMICO": "Ropa Térmica",
    "TERMICO": "Ropa Térmica",
    "CALZA": "Ropa Térmica",
    "OVEROL DESECHABLE": "Ropa Desechable",
    "BUZO DESECHABLE": "Ropa Desechable",
    "MANGA DESECHABLE": "Ropa Desechable",
    "DELANTAL DESECHABLE": "Ropa Desechable",
    "COFIA": "Ropa Desechable",
    "COFIAS DESECHABLE": "Ropa Desechable",
    "PECHERA DESCARNE": "Ropa de Cuero y PVC",
    "COTONA CUERO": "Ropa de Cuero y PVC",
    "COTONA SOLDADOR": "Ropa de Cuero y PVC",
    "DELANTAL CUERO": "Ropa de Cuero y PVC",
    "PANTALÓN": "Ropa de Trabajo - Pantalones",
    "PANTALON": "Ropa de Trabajo - Pantalones",
    "SLACK": "Ropa de Trabajo - Pantalones",
    "POLERA": "Ropa de Trabajo - Poleras",
    "POLERON": "Ropa de Trabajo - Polerones",
    "SWEATER": "Ropa de Trabajo - Polerones",
    "CAMISA": "Ropa de Trabajo - Camisas y Blusas",
    "BLUSA": "Ropa de Trabajo - Camisas y Blusas",
    "CORTAVIENTO": "Ropa de Trabajo - Chaquetas y Parkas",
    "CASACA": "Ropa de Trabajo - Chaquetas y Parkas",
    "CHAQUETA": "Ropa de Trabajo - Chaquetas y Parkas",
    "PARKA": "Ropa de Trabajo - Chaquetas y Parkas",
    "SOFTSHELL": "Ropa de Trabajo - Chalecos y Softshell",
    "CHALECO": "Ropa de Trabajo - Chalecos y Softshell",
    "JARDINERA": "Ropa de Trabajo - Overoles y Buzos",
    "OVEROL": "Ropa de Trabajo - Overoles y Buzos",
    "BUZO": "Ropa de Trabajo - Overoles y Buzos",
    "COTONA": "Ropa de Trabajo - Overoles y Buzos",
    "DELANTAL": "Ropa de Trabajo - Delantales y Pecheras",
    "PECHERA": "Ropa de Trabajo - Delantales y Pecheras",
    "BALACLAVA": "Accesorios de Vestuario",
    "PASAMONTAÑA": "Accesorios de Vestuario",
    "BUFF": "Accesorios de Vestuario",
    "CUELLO": "Accesorios de Vestuario",
    "BANDANA": "Accesorios de Vestuario",
    "GORRO": "Accesorios de Vestuario",
    "JOCKEY": "Accesorios de Vestuario",
    "CALCETA": "Accesorios de Vestuario",
    "CINTURON": "Accesorios de Vestuario",
    "CORBATA": "Accesorios de Vestuario",
    "BANANO": "Bolsos y Mochilas",
    "BOLSO": "Bolsos y Mochilas",
    "MOCHILA": "Bolsos y Mochilas",

    # --- Limpieza / Higiene ---
    "ALCOHOL GEL": "Higiene y Sanitización",
    "ALCOHOL ETILICO": "Higiene y Sanitización",
    "ALCOHOL SPRAY": "Higiene y Sanitización",
    "PAPEL HIGIENICO": "Baño e Higiene",
    "TOALLA PAPEL": "Baño e Higiene",
    "SERVILLETA": "Baño e Higiene",
    "DISPENSADOR DE PAPEL": "Baño e Higiene",
    "DISPENSADOR - TOALLA": "Baño e Higiene",
    "DISPENSADOR - JABON": "Baño e Higiene",
    "DISPENSADOR - ALCOHOL": "Baño e Higiene",
    "BOLSA BASURA": "Limpieza - Basureros y Bolsas",
    "BASURERO": "Limpieza - Basureros y Bolsas",
    "PAPELERO": "Limpieza - Basureros y Bolsas",
    "CONTENEDOR -": "Limpieza - Basureros y Bolsas",
    "BOLSA TNT": "Bolsas y Empaques",
    "CLORO": "Limpieza - Químicos",
    "Cloro": "Limpieza - Químicos",
    "DETERGENTE": "Limpieza - Químicos",
    "Detergente": "Limpieza - Químicos",
    "LAVALOZA": "Limpieza - Químicos",
    "Lavaloza": "Limpieza - Químicos",
    "DESINFECTANTE": "Limpieza - Químicos",
    "Desinfectante": "Limpieza - Químicos",
    "DESENGRASANTE": "Limpieza - Químicos",
    "LIMPIADOR": "Limpieza - Químicos",
    "HIPOCLORITO": "Limpieza - Químicos",
    "AMONIO CUATERNARIO": "Limpieza - Químicos",
    "AROMATIZANTE": "Limpieza - Químicos",
    "CERA": "Limpieza - Químicos",
    "DISCO INODORO": "Baño e Higiene",
    "ESCOBA": "Limpieza - Implementos",
    "ESCOBILLON": "Limpieza - Implementos",
    "BARRE AGUA": "Limpieza - Implementos",
    "MOPA": "Limpieza - Implementos",
    "TRAPERO": "Limpieza - Implementos",
    "PAÑO": "Limpieza - Implementos",
    "ESPONJA": "Limpieza - Implementos",
    "BALDE": "Limpieza - Implementos",
    "COLETO": "Limpieza - Implementos",
    "LIMPIAVIDRIO": "Limpieza - Implementos",
    "LIMPIA VIDRIO": "Limpieza - Implementos",
    "CARRO ESTRUJADOR": "Limpieza - Equipos",
    "BOTELLA -": "Envases y Dispensadores",
    "BIDON": "Envases y Dispensadores",
    "ATOMIZADOR": "Envases y Dispensadores",
    "PISTOLA SPRAY": "Envases y Dispensadores",
    "FLIP TOP": "Envases y Dispensadores",
    "DISPENSADOR AGUA": "Dispensadores de Agua",
    "DISPENSADOR DE AGUA": "Dispensadores de Agua",
    "CAJA ORGANIZADORA": "Organización y Almacenamiento",
    "WENBOX": "Organización y Almacenamiento",

    # --- Mascotas / Abarrotes ---
    "ALIMENTO PARA PERRO": "Mascotas - Alimento",
    "ALIMENTO PARA GATO": "Mascotas - Alimento",
    "AGUA - BOLLENES": "Abarrotes - Agua y Bebidas",
    "AGUA - BIDON": "Abarrotes - Agua y Bebidas",
    "AGUA - BOTELLON": "Abarrotes - Agua y Bebidas",

    # --- Piscinas ---
    "PISC": "Piscinas",
    "PISCINA": "Piscinas",
    "CLORO GRANULADO": "Piscinas",
    "TABLETA CLORO": "Piscinas",
    "ALGUICIDA": "Piscinas",
    "SKIMMER": "Piscinas",
    "DRENO DE FONDO": "Piscinas",
    "RETORNO": "Piscinas",
    "ASPIRACION": "Piscinas",
    "CEPILLO PISCINA": "Piscinas",
    "MANGUERA PISCINA": "Piscinas",
    "BOMBA PISCINA": "Piscinas",
    "FILTRO PISCINA": "Piscinas",
    "DOSIFICADOR CLORO": "Piscinas",
    "PASTA PARA PISCINA": "Piscinas",

    # --- Pesca ---
    "HILO NYLON PESCA": "Pesca",
    "MONOFILAMENTO PESCA": "Pesca",
    "CAÑA": "Pesca",
    "CUCHARILLA": "Pesca",
    "PESCA": "Pesca",

    # --- Ferretería ---
    "SIERRA CIRCULAR": "Ferretería - Herramientas Eléctricas",
    "SIERRA CALADORA": "Ferretería - Herramientas Eléctricas",
    "INGLETADORA": "Ferretería - Herramientas Eléctricas",
    "TRONZADORA": "Ferretería - Herramientas Eléctricas",
    "ROTOMARTILLO": "Ferretería - Herramientas Eléctricas",
    "TALADRO": "Ferretería - Herramientas Eléctricas",
    "ATORNILLADOR": "Ferretería - Herramientas Eléctricas",
    "AMOLADORA": "Ferretería - Herramientas Eléctricas",
    "ESMERIL": "Ferretería - Herramientas Eléctricas",
    "LIJADORA": "Ferretería - Herramientas Eléctricas",
    "HIDROLAVADORA": "Ferretería - Herramientas Eléctricas",
    "ASPIRADORA": "Ferretería - Herramientas Eléctricas",
    "MARTILLO": "Ferretería - Herramientas Manuales",
    "DESTORNILLADOR": "Ferretería - Herramientas Manuales",
    "ALICATE": "Ferretería - Herramientas Manuales",
    "PINZA": "Ferretería - Herramientas Manuales",
    "TENAZA": "Ferretería - Herramientas Manuales",
    "SERRUCHO": "Ferretería - Herramientas Manuales",
    "CUTTER": "Ferretería - Herramientas Manuales",
    "CARTONERO": "Ferretería - Herramientas Manuales",
    "HUINCHA": "Ferretería - Herramientas Manuales",
    "CINTA METRICA": "Ferretería - Herramientas Manuales",
    "NIVEL": "Ferretería - Herramientas Manuales",
    "ESCUADRA": "Ferretería - Herramientas Manuales",
    "FORMON": "Ferretería - Herramientas Manuales",
    "CINCEL": "Ferretería - Herramientas Manuales",
    "CORTAFRIO": "Ferretería - Herramientas Manuales",
    "LIMA": "Ferretería - Herramientas Manuales",
    "TIJERA PODAR": "Ferretería - Herramientas Manuales",
    "PALA": "Ferretería - Herramientas Manuales",
    "RASTRILLO": "Ferretería - Herramientas Manuales",
    "AZADON": "Ferretería - Herramientas Manuales",
    "MACHETE": "Ferretería - Herramientas Manuales",
    "LLAVE COMBINACION": "Ferretería - Herramientas Manuales - Llaves y Dados",
    "LLAVE CHICHARRA": "Ferretería - Herramientas Manuales - Llaves y Dados",
    "LLAVE AJUSTABLE": "Ferretería - Herramientas Manuales - Llaves y Dados",
    "LLAVE ALLEN": "Ferretería - Herramientas Manuales - Llaves y Dados",
    "DADO": "Ferretería - Herramientas Manuales - Llaves y Dados",
    "1/2 DR": "Ferretería - Herramientas Manuales - Llaves y Dados",
    "3/8 DR": "Ferretería - Herramientas Manuales - Llaves y Dados",
    "SIERRA COPA": "Ferretería - Accesorios para Herramientas",
    "HOJA SIERRA": "Ferretería - Accesorios para Herramientas",
    "HOJA DE SIERRA": "Ferretería - Accesorios para Herramientas",
    "HOJA CALADORA": "Ferretería - Accesorios para Herramientas",
    "PUNTA PHILLIPS": "Ferretería - Accesorios para Herramientas",
    "PUNTA TORX": "Ferretería - Accesorios para Herramientas",
    "PUNTA POZI": "Ferretería - Accesorios para Herramientas",
    "PUNTA": "Ferretería - Accesorios para Herramientas",
    "BROCA": "Ferretería - Accesorios para Herramientas",
    "DISCO CORTE": "Ferretería - Abrasivos",
    "DISCO DESBASTE": "Ferretería - Abrasivos",
    "DISCO FLAP": "Ferretería - Abrasivos",
    "DISCO DIAMANTADO": "Ferretería - Abrasivos",
    "LIJA": "Ferretería - Abrasivos",
    "PASTA PULIR": "Ferretería - Abrasivos",
    "CEPILLO METALICO": "Ferretería - Abrasivos",

    # --- Pinturas / Adhesivos ---
    "PISTOLA PARA PINTAR": "Pinturas y Accesorios",
    "CINTA ENMASCARAR": "Pinturas y Accesorios",
    "ENMASCARAR": "Pinturas y Accesorios",
    "RODILLO": "Pinturas y Accesorios",
    "BROCHA": "Pinturas y Accesorios",
    "BANDEJA": "Pinturas y Accesorios",
    "ESPATULA": "Pinturas y Accesorios",
    "STAIN": "Pinturas y Accesorios",
    "BARNIZ": "Pinturas y Accesorios",
    "LATEX": "Pinturas y Accesorios",
    "ESMALTE": "Pinturas y Accesorios",
    "PINTURA": "Pinturas y Accesorios",
    "SILICONA EN BARRA": "Adhesivos y Selladores",
    "PISTOLA SILICONA": "Adhesivos y Selladores",
    "SILICONA": "Adhesivos y Selladores",
    "SELLADOR": "Adhesivos y Selladores",
    "ADHESIVO CERAMICA": "Cerámicas y Revestimientos",
    "ADHESIVO": "Adhesivos y Selladores",
    "PEGAMENTO": "Adhesivos y Selladores",
    "EPOXI": "Adhesivos y Selladores",
    "UNIPOX": "Adhesivos y Selladores",
    "LA GOTITA": "Adhesivos y Selladores",
    "SIKAFLEX": "Adhesivos y Selladores",
    "TEFLON": "Gasfitería - Sellos y Cintas",
    "CINTA DOBLE": "Adhesivos y Selladores",
    "CINTA ALUMINIO PARA POLICARBONATO": "Policarbonato y Techumbres",

    # --- Electricidad ---
    "TABLERO ELECTRICO": "Electricidad - Tableros y Protecciones",
    "DISYUNTOR": "Electricidad - Tableros y Protecciones",
    "DIFERENCIAL": "Electricidad - Tableros y Protecciones",
    "AUTOMATICO": "Electricidad - Tableros y Protecciones",
    "GUARDAMOTOR": "Electricidad - Tableros y Protecciones",
    "FUSIBLE": "Electricidad - Tableros y Protecciones",
    "PORTAFUSIBLE": "Electricidad - Tableros y Protecciones",
    "CONDENSADOR": "Electricidad - Componentes",
    "CAPACITOR": "Electricidad - Componentes",
    "BARRA TOMATIERRA": "Electricidad - Puesta a Tierra",
    "TOMA TIERRA": "Electricidad - Puesta a Tierra",
    "JABALINA": "Electricidad - Puesta a Tierra",
    "PLACA CIEGA": "Electricidad - Enchufes e Interruptores",
    "PLACA SIMPLE": "Electricidad - Enchufes e Interruptores",
    "PLACA DOBLE": "Electricidad - Enchufes e Interruptores",
    "PLACA TRIPLE": "Electricidad - Enchufes e Interruptores",
    "MODULO INTERRUPTOR": "Electricidad - Enchufes e Interruptores",
    "MODULO ENCHUFE": "Electricidad - Enchufes e Interruptores",
    "INTERRUPTOR": "Electricidad - Enchufes e Interruptores",
    "ENCHUFE": "Electricidad - Enchufes e Interruptores",
    "TOMACORRIENTE": "Electricidad - Enchufes e Interruptores",
    "TOMA CORRIENTE": "Electricidad - Enchufes e Interruptores",
    "CINTA AISLADORA": "Electricidad - Accesorios",
    "CONECTOR EMT": "Electricidad - Canalización",
    "CONDUIT": "Electricidad - Canalización",
    "TUBO CONDUIT": "Electricidad - Canalización",
    "TUBO EMT": "Electricidad - Canalización",
    "CANALETA PVC": "Electricidad - Canalización",
    "CAJA DERIVACION": "Electricidad - Canalización",
    "CAJA DE PASO": "Electricidad - Canalización",
    "CABLE THHN": "Electricidad - Cables y Conductores",
    "CABLE HALOGENO": "Electricidad - Cables y Conductores",
    "ALARGADOR": "Electricidad - Extensiones y Alargadores",
    "PANEL LED": "Iluminación",
    "TUBO LED": "Iluminación",
    "AMPOLLETA": "Iluminación",
    "FOCO": "Iluminación",
    "REFLECTOR": "Iluminación",
    "LUMINARIA": "Iluminación",
    "APLIQUE": "Iluminación",

    # --- Gasfitería ---
    "CARTUCHO REPUESTO FILTRO": "Filtración y Tratamiento de Agua",
    "CONTENEDOR 10\" FLOWMAK PARA FILTRO": "Filtración y Tratamiento de Agua",
    "TAPAGORRO": "Gasfitería - Conexiones y Fittings",
    "BUSHING": "Gasfitería - Conexiones y Fittings",
    "NIPLE": "Gasfitería - Conexiones y Fittings",
    "REDUCCION": "Gasfitería - Conexiones y Fittings",
    "COPLA": "Gasfitería - Conexiones y Fittings",
    "CODO": "Gasfitería - Conexiones y Fittings",
    "TEE ": "Gasfitería - Conexiones y Fittings",
    "UNION AMERICANA": "Gasfitería - Conexiones y Fittings",
    "VALVULA": "Gasfitería - Válvulas y Llaves",
    "LLAVE DE PASO": "Gasfitería - Válvulas y Llaves",
    "LLAVE PASO": "Gasfitería - Válvulas y Llaves",
    "LLAVE BOLA": "Gasfitería - Válvulas y Llaves",
    "LLAVE ANGULAR": "Gasfitería - Válvulas y Llaves",
    "MONOMANDO": "Gasfitería - Grifería",
    "GRIFERIA": "Gasfitería - Grifería",
    "FLEXIBLE": "Gasfitería - Grifería",
    "DUCHA": "Gasfitería - Baño y Cocina",
    "SHOWER": "Gasfitería - Baño y Cocina",
    "VANITORIO": "Gasfitería - Baño y Cocina",
    "LAVAMANOS": "Gasfitería - Baño y Cocina",
    "LAVAPLATOS": "Gasfitería - Baño y Cocina",
    "INODORO": "Gasfitería - Baño y Cocina",
    "ASIENTO WC": "Gasfitería - Baño y Cocina",
    "TAPA WC": "Gasfitería - Baño y Cocina",
    "WC": "Gasfitería - Baño y Cocina",
    "SIFON": "Gasfitería - Desagües y Sifones",
    "DESAGUE": "Gasfitería - Desagües y Sifones",
    "BOMBA VACIO": "Bombas y Presurización",
    "BOMBA PRESURIZADORA": "Bombas y Presurización",
    "CONTROLADOR DE PRESION": "Bombas y Presurización",
    "PRESURIZADOR": "Bombas y Presurización",
    "HIDROPACK": "Bombas y Presurización",
    "BOMBA": "Bombas y Presurización",

    # --- Jardinería ---
    "CONTROLADOR RIEGO": "Riego y Jardinería",
    "PROGRAMADOR": "Riego y Jardinería",
    "ELECTROVALVULA": "Riego y Jardinería",
    "VALVULA SOLENOIDE": "Riego y Jardinería",
    "ASPERSOR": "Riego y Jardinería",
    "GOTERO": "Riego y Jardinería",
    "MICROTUBO": "Riego y Jardinería",
    "MANGUERA": "Riego y Jardinería",
    "PULVERIZADOR": "Riego y Jardinería",
    "REGADOR": "Riego y Jardinería",
    "SEMILLA": "Semillas y Jardín",
    "FERTILIZANTE": "Semillas y Jardín",
    "TIERRA": "Semillas y Jardín",
    "HUMUS": "Semillas y Jardín",
    "MACETA": "Semillas y Jardín",
    "INSECTICIDA": "Control de Plagas",
    "RODENTICIDA": "Control de Plagas",
    "CEBADORA": "Control de Plagas",
    "REPELENTE": "Control de Plagas",

    # --- Construcción ---
    "PLANCHA YESO CARTON": "Construcción - Tabiquería y Yeso Cartón",
    "VOLCANITA": "Construcción - Tabiquería y Yeso Cartón",
    "MONTANTE": "Construcción - Tabiquería y Yeso Cartón",
    "PERFIL METALCOM": "Construcción - Metales y Perfilería",
    "METALCOM": "Construcción - Metales y Perfilería",
    "TABLERO OSB": "Construcción - Maderas y Tableros",
    "OSB": "Construcción - Maderas y Tableros",
    "TERCIADO": "Construcción - Maderas y Tableros",
    "MDF": "Construcción - Maderas y Tableros",
    "PINO": "Construcción - Maderas y Tableros",
    "FIERRO": "Construcción - Metales y Perfilería",
    "PLATINA": "Construcción - Metales y Perfilería",
    "ANGULO": "Construcción - Metales y Perfilería",
    "PERFIL CUADRADO": "Construcción - Metales y Perfilería",
    "PERFIL": "Construcción - Metales y Perfilería",
    "BEFRAGUE": "Construcción - Cerámicas y Revestimientos",
    "FRAGUE": "Construcción - Cerámicas y Revestimientos",
    "PORCELANATO": "Construcción - Cerámicas y Revestimientos",
    "CERAMICA": "Construcción - Cerámicas y Revestimientos",
    "PISO VINILICO": "Construcción - Cerámicas y Revestimientos",
    "SEPARADOR CERAMICA": "Construcción - Cerámicas y Revestimientos",
    "POLICARBONATO": "Construcción - Policarbonato y Techumbres",
    "PLANCHA ZINC": "Construcción - Techumbre y Canaletas",
    "CANALETA PH25": "Construcción - Techumbre y Canaletas",
    "BAJADA CANALETA": "Construcción - Techumbre y Canaletas",
    "UNION CANALETA": "Construcción - Techumbre y Canaletas",
    "CUMBRERA": "Construcción - Techumbre y Canaletas",
    "CABALLETE": "Construcción - Techumbre y Canaletas",
    "MEMBRANA ASFALTICA": "Construcción - Impermeabilización y Membranas",
    "MEMBRANA": "Construcción - Impermeabilización y Membranas",
    "AISLAPOL": "Construcción - Aislación",

    # --- Cerrajería / Herrajes ---
    "TOALLERO": "Baño - Accesorios",
    "PORTARROLLO": "Baño - Accesorios",
    "JABONERA": "Baño - Accesorios",
    "BARRA SEGURIDAD": "Baño - Accesorios",
    "CORTINA BAÑO": "Baño - Accesorios",
    "CORTINA DE BAÑO": "Baño - Accesorios",
    "ESPEJO LED": "Baño - Accesorios",
    "CANDADO": "Cerrajería y Herrajes",
    "CERROJO": "Cerrajería y Herrajes",
    "PASADOR": "Cerrajería y Herrajes",
    "PICAPORTE": "Cerrajería y Herrajes",
    "MANILLA": "Cerrajería y Herrajes",
    "POMO": "Cerrajería y Herrajes",
    "PERILLA": "Cerrajería y Herrajes",
    "BISAGRA": "Cerrajería y Herrajes",
    "CIERRAPUERTA": "Cerrajería y Herrajes",
    "CIERRA PUERTA": "Cerrajería y Herrajes",
    "CERRADURA": "Cerrajería y Herrajes",

    # --- Fijaciones ---
    "ROSCALATA": "Fijaciones y Tornillos",
    "AUTOPERFORANTE": "Fijaciones y Tornillos",
    "TIRAFONDO": "Fijaciones y Tornillos",
    "TORNILLO": "Fijaciones y Tornillos",
    "PERNO": "Fijaciones y Tornillos",
    "TUERCA": "Fijaciones y Tornillos",
    "ARANDELA": "Fijaciones y Tornillos",
    "REMACHE": "Fijaciones y Tornillos",
    "CLAVO": "Fijaciones y Tornillos",
    "GRAPA": "Fijaciones y Tornillos",
    "TARUGO": "Anclajes y Tarugos",
    "ANCLAJE": "Anclajes y Tarugos",
    "ABRAZADERA": "Sujeción y Abrazaderas",

    # --- Transporte / Soldadura / Automotriz / Electrónica ---
    "CARRETILLA": "Carretillas y Transporte",
    "RUEDA CARRETILLA": "Carretillas y Transporte",
    "DIABLO": "Carretillas y Transporte",
    "ESCALERA": "Escaleras y Andamios",
    "SOPLETE": "Soldadura y Gas",
    "ELECTRODO": "Soldadura y Gas",
    "SOLDADURA": "Soldadura y Gas",
    "GAS BUTANO CARTUCHO": "Soldadura y Gas",
    "CARTUCHO GAS": "Soldadura y Gas",
    "WD-40": "Lubricantes y Químicos Automotrices",
    "WD40": "Lubricantes y Químicos Automotrices",
    "AFLOJATODO": "Lubricantes y Químicos Automotrices",
    "ACEITE": "Lubricantes y Químicos Automotrices",
    "GRASA": "Lubricantes y Químicos Automotrices",
    "LUBRICANTE": "Lubricantes y Químicos Automotrices",
    "SILICONA TABLERO": "Lubricantes y Químicos Automotrices",
    "CABLE HDMI": "Electrónica y Conectividad",
    "CABLE UTP": "Electrónica y Conectividad",
    "CONECTOR RJ45": "Electrónica y Conectividad",
    "MOUSE": "Electrónica y Conectividad",

    # =========================
    # 🛡️ REGLAS GENERALES (Al final para que no interfieran)
    # =========================
    "FERR.": "Ferretería General",
    "FERR": "Ferretería General",
}

# --- CACHÉ (Para no preguntar 1000 veces lo mismo a la web) ---
cache_ids_categorias = {}

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }


# ==============================================================================
# 🔄 REGLAS DE VENTA CRUZADA (CROSS-SELL)
# Si cae en la categoría (KEY), sugerimos productos de las categorías (VALUE)
# ==============================================================================
REGLAS_CROSS_SELL = {
    # --- Ferretería ---
    "Pinturas y Accesorios": ["Adhesivos y Selladores", "Ferretería - Herramientas Manuales", "Pinturas y Accesorios"],
    "Ferretería - Herramientas Eléctricas": ["Ferretería - Accesorios para Herramientas", "EPP - Protección Ocular", "Electricidad - Extensiones y Alargadores"],
    "Ferretería - Herramientas Manuales": ["Ferretería - Accesorios para Herramientas", "Organización y Almacenamiento"],
    "Soldadura y Gas": ["EPP - Protección Facial", "Ropa de Cuero y PVC", "Ferretería - Abrasivos"],
    
    # --- Construcción ---
    "Construcción - Cerámicas y Revestimientos": ["Adhesivos y Selladores", "Ferretería - Herramientas Manuales"], 
    "Construcción - Techumbre y Canaletas": ["Ferretería - Fijaciones y Tornillos", "Adhesivos y Selladores"],
    "Construcción - Tabiquería y Yeso Cartón": ["Ferretería - Fijaciones y Tornillos", "Construcción - Aislación"],

    # --- EPP ---
    "EPP - Protección de Cabeza": ["EPP - Protección Auditiva", "EPP - Protección Ocular", "Accesorios de Vestuario"],
    "EPP - Protección Ocular": ["EPP - Limpieza de Lentes", "EPP - Protección de Cabeza"],
    "Calzado de Seguridad": ["Accesorios de Calzado", "Accesorios de Vestuario", "Ropa de Trabajo - Pantalones"],
    "Protección contra Caídas": ["EPP - Protección de Cabeza", "Ferretería - Herramientas Manuales"],
    
    # --- Limpieza ---
    "Baño e Higiene": ["Baño - Accesorios", "Limpieza - Basureros y Bolsas", "Higiene y Sanitización"],
    "Limpieza - Químicos": ["Limpieza - Implementos", "EPP - Protección de Manos - Desechables"],
    "Limpieza - Basureros y Bolsas": ["Limpieza - Basureros y Bolsas"], # Bolsa sugiere Basurero
    
    # --- Piscinas ---
    "Piscinas": ["Piscinas"] # Todo piscina se sugiere entre sí
}

# Caché para guardar IDs de productos sugeridos por categoría
# Formato: { "Nombre Categoría": [id1, id2, id3] }
cache_productos_sugeridos = {}

def obtener_o_cargar_cross_sells(categoria_actual_nombre):
    """
    Busca IDs de productos para cross-sell basados en las reglas.
    Si no están en caché, los busca en la API (SOLO UNA VEZ por categoría).
    """
    ids_finales = []
    
    # 1. Ver qué categorías sugerir según la regla
    # Si no hay regla específica, no sugerimos nada para no spammear
    categorias_a_sugerir = REGLAS_CROSS_SELL.get(categoria_actual_nombre, [])
    
    if not categorias_a_sugerir:
        return []

    # 2. Iterar sobre las categorías sugeridas
    for cat_sugerida in categorias_a_sugerir:
        # Si ya hemos buscado productos para esta categoría antes, USAMOS LA CACHÉ
        if cat_sugerida in cache_productos_sugeridos:
            ids_finales.extend(cache_productos_sugeridos[cat_sugerida])
            continue
            
        # Si no, vamos a buscar a la API unos 3 productos de esa categoría
        # Primero necesitamos el ID de la categoría sugerida
        id_cat_sugerida = buscar_o_crear_categoria(cat_sugerida)
        
        if id_cat_sugerida:
            try:
                # Traemos 4 productos de esa categoria
                url = f"{WOO_URL}/wp-json/wc/v3/products?category={id_cat_sugerida}&per_page=4"
                r = requests.get(url, headers=get_headers(), timeout=15)
                if r.status_code == 200:
                    prods = r.json()
                    ids_encontrados = [p['id'] for p in prods]
                    
                    # Guardamos en caché para no volver a preguntar
                    cache_productos_sugeridos[cat_sugerida] = ids_encontrados
                    ids_finales.extend(ids_encontrados)
                    print(f"        Aprendidos {len(ids_encontrados)} sugeridos de '{cat_sugerida}'")
                else:
                    cache_productos_sugeridos[cat_sugerida] = [] # Evitar reintentar fallos
            except:
                pass
        else:
            cache_productos_sugeridos[cat_sugerida] = [] # No existe la cat
            
    # Devolvemos una lista limpia (máximo 4 sugerencias en total para no saturar)
    return ids_finales[:4]

def buscar_o_crear_categoria(nombre_categoria):
    # Si ya tenemos la ruta completa en caché, devolvemos el ID final directamente
    if nombre_categoria in cache_ids_categorias:
        return cache_ids_categorias[nombre_categoria]
    
    partes = nombre_categoria.split(" - ")
    id_padre = 0 # 0 es la raíz en WooCommerce
    
    for parte in partes:
        parte = parte.strip() # Limpieza de espacios extra
        encontrado_id = None
        
        try:
            # 1. Buscar si existe esta parte (filtrando luego por padre)
            # Usamos search para acotar, pero la validación final es estricta
            url_search = f"{WOO_URL}/wp-json/wc/v3/products/categories?search={parte}"
            r = requests.get(url_search, headers=get_headers(), timeout=20)
            
            if r.status_code == 200:
                candidatos = r.json()
                for cat in candidatos:
                    # Validamos nombre EXACTO y que pertenezca al padre actual
                    # cat['parent'] devuelve el ID del padre (0 si es raíz)
                    if cat['name'].lower() == parte.lower() and cat['parent'] == id_padre:
                        encontrado_id = cat['id']
                        break
        except Exception as e:
            print(f"    Error buscando categoria '{parte}': {e}")
            time.sleep(1)

        # 2. Si no existe, crearla asociada al padre actual
        if not encontrado_id:
            print(f"    Creando sub-categoria: '{parte}' bajo ID padre: {id_padre}")
            try:
                url_create = f"{WOO_URL}/wp-json/wc/v3/products/categories"
                data = {
                    "name": parte,
                    "parent": id_padre
                }
                r_create = requests.post(url_create, headers=get_headers(), json=data, timeout=20)
                
                if r_create.status_code == 201:
                    encontrado_id = r_create.json()['id']
                else:
                    print(f"    Error al crear '{parte}': {r_create.text}")
                    # Si falla un nivel, no podemos seguir con los hijos
                    return None
            except Exception as e:
                print(f"    Error creando '{parte}': {e}")
                return None
        
        # El hijo actual se convierte en el padre del siguiente nivel
        id_padre = encontrado_id

    # Al terminar el bucle, id_padre es la categoría final
    if id_padre:
        cache_ids_categorias[nombre_categoria] = id_padre
        return id_padre
    
    return None

    return None

# --- CONTROL DE PROGRESO ---
ESTADO_FILE = "estado_progreso.json"

def cargar_progreso():
    try:
        with open(ESTADO_FILE, "r") as f:
            data = json.load(f)
            return data.get("pagina", 1)
    except:
        return 1

def guardar_progreso(pagina):
    try:
        with open(ESTADO_FILE, "w") as f:
            json.dump({"pagina": pagina}, f)
    except Exception as e:
        print(f" Error guardando progreso: {e}")

def limpiar_categorias_vacias():
    print("\n------------------------------------------------")
    print(" INICIANDO LIMPIEZA DE CATEGORIAS VACIAS")
    print("------------------------------------------------")
    
    page_cat = 1
    ids_a_borrar = []
    
    while True:
        try:
            url = f"{WOO_URL}/wp-json/wc/v3/products/categories?per_page=100&page={page_cat}"
            r = requests.get(url, headers=get_headers(), timeout=30)
            
            if r.status_code != 200:
                break
                
            categorias = r.json()
            if not categorias:
                break
                
            for cat in categorias:
                # Si count es 0 y no es Uncategorized
                if cat['count'] == 0 and cat['slug'] != 'uncategorized':
                     ids_a_borrar.append({'id': cat['id'], 'name': cat['name']})
            
            page_cat += 1
            
        except Exception as e:
            print(f" Error escaneando categorias: {e}")
            break
            
    print(f" Se encontraron {len(ids_a_borrar)} categorias vacias para eliminar.")
    
    for item in ids_a_borrar:
        cat_id = item['id']
        cat_name = item['name']
        print(f"    Borrando: [{cat_id}] {cat_name}")
        
        try:
            url_delete = f"{WOO_URL}/wp-json/wc/v3/products/categories/{cat_id}?force=true"
            requests.delete(url_delete, headers=get_headers(), timeout=10)
            time.sleep(0.5) 
        except Exception as e:
            print(f"    Error borrando {cat_id}: {e}")

    print(" Limpieza finalizada.")

def main():
    print("------------------------------------------------")
    print("AUTO-ORGANIZADOR DE CATEGORIAS (MODO ANTI-CRASH)")
    print("------------------------------------------------")
    
    # Cargar pagina desde archivo
    page = cargar_progreso()
    print(f" Reanudando proceso desde la pagina {page}...")
    
    modificados = 0
    errores_consecutivos = 0
    
    while True:
        try:
            print(f"\n Leyendo pagina {page} de productos...")
            url = f"{WOO_URL}/wp-json/wc/v3/products?per_page=50&page={page}"
            
            # Timeout aumentado a 30 segundos
            r = requests.get(url, headers=get_headers(), timeout=30)
            
            if r.status_code != 200:
                print(f" Error leyendo pagina (Status {r.status_code}). Terminando.")
                break
                
            productos = r.json()
            if not productos:
                print(" Fin del inventario.")
                break
            
            # Reiniciamos contador de errores si la página cargó bien
            errores_consecutivos = 0 

            for p in productos:
                pid = p['id']
                nombre = p['name']
                
                categoria_destino = None
                for palabra_clave, nombre_cat_destino in MAPA_CATEGORIAS.items():
                    if palabra_clave.lower() in nombre.lower():
                        categoria_destino = nombre_cat_destino
                        break 
                
                if categoria_destino:
                    print(f"    [{pid}] {nombre}") 
                    
                    id_cat = buscar_o_crear_categoria(categoria_destino)
                    
                    if id_cat:
                        # --- REMOVIDA LÓGICA DE SALTAR ---
                        # Queremos forzar la actualización para limpiar categorías viejas
                        # y asegurar que los cross-sells se apliquen.
                        # --------------------------------------

                        print(f"        Asignando a: '{categoria_destino}'")

                        # INTENTO DE ACTUALIZACIÓN CON PROTECCIÓN
                        try:
                            url_update = f"{WOO_URL}/wp-json/wc/v3/products/{pid}"
                            
                            # LOGICA DE CROSS-SELL
                            ids_cross_sell = obtener_o_cargar_cross_sells(categoria_destino)
                            
                            data_update = {
                                "categories": [{"id": id_cat}]
                            }
                            
                            # Si encontramos sugerencias, las agregamos
                            if ids_cross_sell:
                                # Filtramos para no sugerirse a sí mismo
                                ids_cross_sell = [i for i in ids_cross_sell if i != pid]
                                if ids_cross_sell:
                                    data_update["cross_sell_ids"] = ids_cross_sell
                                    print(f"        Vinculando {len(ids_cross_sell)} productos sugeridos.")

                            # Timeout de 15s y espera posterior
                            requests.put(url_update, headers=get_headers(), json=data_update, timeout=15)
                            modificados += 1
                            
                            # 🛑 FRENO DE MANO: Pausa de 0.5 seg para no matar el servidor
                            time.sleep(0.5) 
                            
                        except Exception as e_up:
                            print(f"        Timeout al actualizar ID {pid}. Saltando...")
                            time.sleep(2) # Pausa de seguridad
            
            # Guardamos el progreso de la SIGUIENTE pagina a procesar
            page += 1
            guardar_progreso(page)
            
            
        except Exception as e_page:
            print(f" Error grave leyendo pagina {page}: {e_page}")
            errores_consecutivos += 1
            print(" Esperando 10 segundos antes de reintentar...")
            time.sleep(10)
            
            if errores_consecutivos > 3:
                print(" Demasiados errores seguidos. Abortando.")
                break
    
    print(f"\n Listo! Se organizaron {modificados} productos.")
    
    # Ejecutar limpieza final
    limpiar_categorias_vacias()
    

if __name__ == "__main__":
    main()