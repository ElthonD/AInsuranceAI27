import database_ainsurance as ainsurance_db

fechas = ['22/06/2023','28/06/2023','30/06/2023','04/08/2023','06/08/2023','06/08/2023','07/08/2023','07/08/2023','09/08/2023','10/08/2023','11/08/2023','15/08/2023','16/08/2023','18/08/2023','23/08/2023','29/08/2023','29/08/2023','30/08/2023','30/08/2023','31/08/2023','31/08/2023','02/09/2023','12/09/2023','12/09/2023','29/09/2023','03/10/2023','04/10/2023','06/10/2023','10/10/2023','11/10/2023','11/10/2023','17/10/2023','18/10/2023','20/10/2023','21/10/2023','25/10/2023','26/10/2023','29/10/2023','30/10/2023','31/10/2023','06/11/2023','13/11/2023','15/11/2023','15/11/2023','17/11/2023','18/11/2023','18/11/2023','20/11/2023','20/11/2023','24/11/2023','24/11/2023','28/11/2023','13/10/2023','14/09/2023','11/11/2023','29/11/2023','08/11/2023','07/01/2023','01/02/2023','07/02/2023','10/02/2023','03/03/2023','08/03/2023','19/05/2023','27/06/2023','28/07/2023','18/09/2023','21/09/2023','07/10/2023','21/10/2023','06/11/2023','19/11/2023','28/11/2023','08/11/2023','08/11/2023','12/04/2023','18/04/2023','09/08/2023']
#fechas = [datetime.datetime(2023, 6, 22, 0, 0), datetime.datetime(2023, 6, 28, 0, 0), datetime.datetime(2023, 6, 30, 0, 0), datetime.datetime(2023, 8, 4, 0, 0), datetime.datetime(2023, 8, 6, 0, 0), datetime.datetime(2023, 8, 6, 0, 0), datetime.datetime(2023, 8, 7, 0, 0), datetime.datetime(2023, 8, 7, 0, 0), datetime.datetime(2023, 8, 9, 0, 0), datetime.datetime(2023, 8, 10, 0, 0), datetime.datetime(2023, 8, 11, 0, 0), datetime.datetime(2023, 8, 15, 0, 0), datetime.datetime(2023, 8, 16, 0, 0), datetime.datetime(2023, 8, 18, 0, 0), datetime.datetime(2023, 8, 23, 0, 0), datetime.datetime(2023, 8, 29, 0, 0), datetime.datetime(2023, 8, 29, 0, 0), datetime.datetime(2023, 8, 30, 0, 0), datetime.datetime(2023, 8, 30, 0, 0), datetime.datetime(2023, 8, 31, 0, 0), datetime.datetime(2023, 8, 31, 0, 0), datetime.datetime(2023, 9, 2, 0, 0), datetime.datetime(2023, 9, 12, 0, 0), datetime.datetime(2023, 9, 12, 0, 0), datetime.datetime(2023, 9, 29, 0, 0), datetime.datetime(2023, 10, 3, 0, 0), datetime.datetime(2023, 10, 4, 0, 0), datetime.datetime(2023, 10, 6, 0, 0), datetime.datetime(2023, 10, 10, 0, 0), datetime.datetime(2023, 10, 11, 0, 0), datetime.datetime(2023, 10, 11, 0, 0), datetime.datetime(2023, 10, 17, 0, 0), datetime.datetime(2023, 10, 18, 0, 0), datetime.datetime(2023, 10, 20, 0, 0), datetime.datetime(2023, 10, 21, 0, 0), datetime.datetime(2023, 10, 25, 0, 0), datetime.datetime(2023, 10, 26, 0, 0), datetime.datetime(2023, 10, 29, 0, 0), datetime.datetime(2023, 10, 30, 0, 0), datetime.datetime(2023, 10, 31, 0, 0), datetime.datetime(2023, 11, 6, 0, 0), datetime.datetime(2023, 11, 13, 0, 0), datetime.datetime(2023, 11, 15, 0, 0), datetime.datetime(2023, 11, 15, 0, 0), datetime.datetime(2023, 11, 17, 0, 0), datetime.datetime(2023, 11, 18, 0, 0), datetime.datetime(2023, 11, 18, 0, 0), datetime.datetime(2023, 11, 20, 0, 0), datetime.datetime(2023, 11, 20, 0, 0), datetime.datetime(2023, 11, 24, 0, 0), datetime.datetime(2023, 11, 24, 0, 0), datetime.datetime(2023, 11, 28, 0, 0), datetime.datetime(2023, 10, 13, 0, 0), datetime.datetime(2023, 9, 14, 0, 0), datetime.datetime(2023, 11, 11, 0, 0), datetime.datetime(2023, 11, 29, 0, 0), datetime.datetime(2023, 11, 8, 0, 0), datetime.datetime(2023, 1, 7, 0, 0), datetime.datetime(2023, 2, 1, 0, 0), datetime.datetime(2023, 2, 7, 0, 0), datetime.datetime(2023, 2, 10, 0, 0), datetime.datetime(2023, 3, 3, 0, 0), datetime.datetime(2023, 3, 8, 0, 0), datetime.datetime(2023, 5, 19, 0, 0), datetime.datetime(2023, 6, 27, 0, 0), datetime.datetime(2023, 7, 28, 0, 0), datetime.datetime(2023, 9, 18, 0, 0), datetime.datetime(2023, 9, 21, 0, 0), datetime.datetime(2023, 10, 7, 0, 0), datetime.datetime(2023, 10, 21, 0, 0), datetime.datetime(2023, 11, 6, 0, 0), datetime.datetime(2023, 11, 19, 0, 0), datetime.datetime(2023, 11, 28, 0, 0), datetime.datetime(2023, 11, 8, 0, 0), datetime.datetime(2023, 11, 8, 0, 0), datetime.datetime(2023, 4, 12, 0, 0), datetime.datetime(2023, 4, 18, 0, 0), datetime.datetime(2023, 8, 9, 0, 0)]
names = ['David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos', 'David Ramos']
bitacoras = ['Sin Bitácora', 'Sin Bitácora', 'Sin Bitácora', 785015808, 785019397, 785022553, 785022169, 785022173, 785026953, 785031288, 785033677, 785045510, 785050011, 785055612, 'Sin Bitácora', 'Sin Bitácora', 785081713, 785083816, 785086992, 785087013, 795088956, 795094507, 795119222, 795124941, 795167475, '7A5177039', '7A5182100', '7A5185835', '7A5195601 ', '7A5199890', '7A5202590\n', '7A5218496', '7A5219632', '7A5225758', '7A5230114', 'Sin Bitácora', '7A5245313', '7A5252460', '7A5256703', '7A5257813', '7B5278112 ', '7B5294153', '7B5302279', '7B5302314', '7B5309806', '7B5312114', '7B5312368', '7B5317708', '7B5324543', '7B5332453', 'Sin Bitácora', 'Sin Bitácora', '7A5205185\n', 'Sin Bitácora', '7B5290509', 'Sin Bitácora', '7B5280685', '714461402 / 714462172', '724527768 / 714525301', 724543415, '724548407 / 724543415', 734614650, '734621889-734619890', '754810200-754810049', 764915165, '774997726-774993006', 795135232, 795163276, '7A5190269', '7A5229598', '7B5275914', '7B5317717', 'Sin Bitácora', '7B5284850', '7B5284827', 744709010, 744724916, 785028369]
clientes = ['SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'SITRACK', 'AUTOFLETES CHIHUAHUA', 'TGT', 'TGT', 'TGT', 'MAEDA', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'MAVERICK', 'TRANSPORTES MENDEZ', 'TRANSPORTES MENDEZ', 'SETRAMEX', 'SETRAMEX', 'SETRAMEX']
entradas = ['Llamada cliente', 'Correo cliente', 'Bitácora CM ', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente', 'Whatsapp cliente', 'Whatsapp cliente', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente', 'Correo cliente', 'Llamada cliente', 'Whatsapp cliente', 'Llamada cliente', 'Whatsapp cliente', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente', 'Bitácora CM ', 'Llamada cliente', 'Llamada cliente', 'Whatsapp cliente', 'Bitácora CM ', 'Llamada cliente', 'Llamada cliente', 'Whatsapp cliente', 'Llamada cliente', 'Llamada cliente', 'Whatsapp cliente', 'Whatsapp cliente', 'Whatsapp cliente', 'Whatsapp cliente', 'Whatsapp cliente', 'Whatsapp cliente', 'Whatsapp cliente', 'Llamada cliente', 'Bitácora CM ', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente', 'Alerta Telegram', 'Alerta Telegram', 'Alerta Telegram', 'Bitácora CM ', 'Llamada cliente', 'Llamada del cliente', 'Whatsapp cliente', 'Whatsapp cliente', 'Bitácora CM ', 'Bitácora CM ', 'Solicitud de cliente', 'Solicitud de cliente', 'Solicitud de cliente', 'Bitácora CM ', 'Bitácora CM ', 'Bitácora CM ', 'Bitácora CM ', 'Bitácora CM ', 'Bitácora CM ', 'Bitácora CM ', 'Solicitud de cliente', 'Solicitud de cliente', 'Solicitud de cliente', 'Solicitud de cliente', 'Solicitud de cliente', 'Correo cliente', 'Bitácora CM', 'Llamada cliente', 'Llamada cliente', 'Llamada cliente']
marcas = ['KENWORTH', 'KENWORTH', 'INTERNACIONAL', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'INTERNATIONAL', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'INTERNATIONAL', 'INTERNATIONAL', 'FREIGHTLINER', 'KENWORTH', 'KENWORTH', 'FREIGHTLINER', 'INTERNATIONAL', 'FREIGHTLINER', 'KENWORTH', 'VOLVO', 'KENWORTH', 'KENWORTH', 'FREIGHTLINER', 'FREIGHTLINER', 'VOLVO', 'KENWORTH', 'KENWORTH', 'INTERNATIONAL', 'INTERNATIONAL', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'KENWORTH', 'FREIGHTLINER', 'FREIGHTLINER', 'FREIGHTLINER']
modelos = [2023, 2013, 2006, 2021, 2019, 2019, 2023, 2023, 2024, 2021, 2020, 2018, 2019, 2023, 2023, 2024, 2023, 2021, 2015, 2014, 2021, 2021, 2024, 2022, 'No Especificado', 2017, 'No Especificado', 'No Especificado', 2024, 2017, 2020, 2023, 'No Especificado', 2024, 2022, 2022, 2021, 2019, 2018, 2022, 2024, 2020, 2020, 2020, 2023, 2024, 2024, 2023, 2022, 2022, 'No Especificado', 2022, 2024, 'No Especificado', 'No Especificado', 2017, 2022, 2021, 2016, 2018, 2000, 2013, 2000, 2020, 1998, 2023, 2013, 2000, 2021, 2000, 2020, 2000, 2022, 'No Especificado', 2014, 2017, 2017, 2014]
placas = ['53FA7F', '625AT7', '20AX8C', '19AX9H', '43AL3E', '43AL3E', '51AR5Y', '80FA5H', '43BB8K', '24AR2X', '64AM6J', '84AK4P', '44AK6E', '70AZ1A', '78FA8G', '88BA6C/74UM3L', '54AU8K ', '74AP5L', '86AR5A', '33AV4E', '06AP8E', '673FF2', '13BA2M', '38AT5J', '45AU8K', '69AF8E', '950FE8', '22AK8C', '83AY1E', '73AD4W', '76AN9F', '57AN2M', '29AP4C/MAS543199', '42BB3F', '45AP9W', '91AT5J', '29AR1M', '07AH4C', '28AY3L', '69AU8M', '20AZ9D', '82AN2Y', '04BA1X\n', '92AE6Z', '98FA3H', '74AZ9F', '75AZ9F', '79AY5M', '78AP8E', '72AP4W', '99AT3E', '39AS5R', '99AP8L', '99AK4Z', '21AX2B\t', '28AE9J', '41AR2F', '59AT9H', '45AD3G', '195ER9', '14AU1T', '259EP5', '010EY4', '60AU1T', '70AS2P', '89BA2U', '233ER7', '60AU1T', '58AR4Z', '012EY4', '28AB3G', '46AD3G', '68AS2P', '74AU9M', '73AU9M', '25AD1X', '68AP1F', '24AY5E']
economicos = [49, 110, 36, 'SE', 'TNA01', 'TNA01', 164, 'SE', 'EBA22', 7, 'SE', 1137, 'SE', 'SE', 'SE', 'SE', 'SE', 16, 'SE', 'T127', 'SE', 217, 100, 'PR9245', 'SE', 28, 210, 'ST299', 177, 21, 1, 'S/E', 380, 'GX12', 67, 'PR9315', 'T-880', 10, 'SE', 'SE', 5, 14, 'S/E', 27, 'MX054', 25, 27, 22, 204, 127, 'SE', 384, 244, 'T328', 'T356', 'T304', 530, 235, 'RM162', 'RM91', 'RM254', 'RM85', 'RM130', 247, 'RM231', 'RM298', 'RM102', 'RM247', 'RM216', 'RM134', 'RM138', 'RM163', 'RM229', 21, 20, 1788, 1773, 23023]
latitudes = [19.849875, 20.254191, 19.631786, 19.0, 18.864667, 18.864667, 20.080893, 19.108998, 21.050527, 22.003083, 19.968907, 18.438265, 19.0751135, 18.864508, 22.029322, 18.94724, 20.53128, 19.762616, 18.844007, 19.496167, 19.93701, 19.804607, 19.788728, 18.929363, 20.100292, 21.514858, 19.705807, 20.01803, 19.86425, 20.535358, 19.050124, 19.923765, 18.110152, 19.972547, 18.931352, 18.914641, 26.235474, 18.040817, 18.972469, 19.276733, 19.62011, 19.311457, 19.0973889, 20.848714, 19.789995, 22.041627, 19.924703, 19.88293, 20.395563, 19.80359, 21.544569, 19.314738, 21.99009, 19.57274878, 22.46812111, 18.977525, 19.6389, 19.2655, 22.026096, 19.697892, 19.587052, 19.382003, 19.438781, 22.98276, 20.752299, 18.356897, 19.891368, 19.667932, 18.880485, 20.121397, 21.195053, 18.402185, 19.978715, 19.618978, 20.578247, 20.535534, 20.549639, 23.129107]
longitudes = [-99.284895, -99.846337, -99.091799, -97.88, -97.388722, -97.388722, -99.64377, -98.186602, -100.481453, -100.844003, -99.05742, -97.422569, -98.2019072, -97.38853, -100.848417, -97.723162, -100.718427, -98.64916, -97.325867, -99.015053, -99.237943, -98.973303, -98.784061, -97.680973, -102.347882, -101.733258, -99.218849, -99.24793, -99.227741, -103.016903, -99.240612, -99.237438, -95.452414, -101.75512, -97.682638, -97.643907, -98.601202, -94.337483, -97.810785, -98.448788, -98.54692, -98.499672, -98.2071389, -103.853555, -99.222407, -98.868918, -99.033238, -99.238328, -100.02349, -99.21948, -100.749464, -98.82096, -100.827452, -98.56097876, -101.52316206, -97.80081, -99.1501, -98.430728, -101.573611, -99.08203, -99.195382, -99.3924, -99.123509, -102.72932, -101.343713, -96.261667, -100.448405, -99.132655, -97.587643, -99.722697, -104.568416, -99.487323, -98.849138, -99.042757, -100.96031, -100.70993, -100.985508, -100.51478]
estados = ['Hidalgo', 'México', 'México', 'Puebla', 'Puebla', 'Puebla', 'México', 'Puebla', 'Guanajuato', 'San Luis Potosi ', 'México', 'Puebla', 'Puebla', 'Puebla', 'San Luis Potosi ', 'Puebla', 'Guanajuato', 'México', 'Puebla', 'México', 'México', 'México', 'México', 'Puebla', 'Michoacán', 'Jalisco', 'México', 'Hidalgo', 'México', 'Jalisco', 'Morelos', 'Hidalgo', 'Veracruz', 'Michoacán', 'Puebla', 'Puebla', 'Tamaulipas', 'Veracruz', 'Puebla', 'Puebla', 'Tlaxcala', 'Puebla', 'Puebla', 'Jalisco', 'México', 'San Luis Potosí', 'México', 'Hidalgo', 'Queretaro', 'México', 'Guanajuato', 'México', 'San Luis Potosí', 'Tlaxcala', 'Zacatecas ', 'Puebla', 'México', 'Puebla', 'Zacatecas', 'México', 'México', 'México', 'Ciudad de México', 'Zacatecas', 'Guanajuato', 'Veracruz', 'Michoacan', 'México', 'Puebla', 'México', 'Nayarit', 'Guerrero', 'Hidalgo', 'México', 'Guanajuato', 'Guanajuato', 'Guanajuato', 'San Luis Potosí']
municipios = ['Tepeji', 'Polotitlán', 'San Pablo de las salinas', 'Tepeaca', 'Esperanza', 'Esperanza', 'Jilotepec', 'Puebla', 'San José Iturbide', 'La pila', 'Santa María Ajolopan', 'Santa María Coapan', 'Santa María La Rivera', 'Esperanza', 'Olivia Martinez Mata', 'Tecamachalco', 'Apaseo el grande', 'Xala', 'Puebla', 'Ecatepec', 'Hidalgo', 'La Palma', 'Aztacameca', 'Quecholac', 'La Sauceda', 'Lagos de Moreno, Jal.', 'Tepozotlan', ' Progreso', ' Santa Teresa', 'La Soledad de Pérez', 'Tres Marías', 'Jorobas - Tula, 42994 Hgo.', 'Juan Rodríguez Clara', ' Panindícuaro, Michoacán', 'Francisco I Madero', '\xa0Palmarito Tochapan', 'Gustavo Díaz Ordaz', 'Ixhuatlán', 'Actipan de Morelos', 'San Martín Texmelucan', 'Calpulalpan', 'San Matías Tlalancaleca', 'Heroica Puebla de Zaragoza', 'Tequila', 'Coyotepec', 'Tamuín', 'Hueypoxtla', 'Santiago Tlaltepoxco', 'San Juan del Río', 'Coyotepec', 'San Pedro', 'Xuexuculco', 'Entronque a Zaragoza', 'Calpulalpan', 'Trinidad Norte ', 'Acatzingo ', 'Tultitlán', 'San Martín Texmelucan', 'Jaula de abajo', 'Paseos del valle', 'Tlalnepantla de Baz', 'San cruz Ayotuzco', 'Lorenzo Boturini', 'Gral Enrique Estrada', 'Hacienda del copal', 'Don Juan', 'Maravatio', 'Tultepec', 'Santa Cruz Ocotlán', 'La Esperanza ', 'Santa María del Oro', 'Cieneguillas', 'Nueva Santa María', 'San Cristóbal, Ecatepec', 'Torrecilla', 'Apaseo el grande', 'Villagrán', 'Villa de Guadalupe']
tramos = ['Tepozotlán - Palmillas', 'Tepozotlán - Palmillas', 'Coacalco', 'Esperanza - Amozoc', 'Esperanza - Amozoc ', 'Esperanza - Amozoc', 'Tepozotlán - Palmillas', 'Zona Sin Asignación de Nombre de Col 1', 'San luis - Chichimequillas', 'Libramiento Poniente SLP', 'Santa María Ajolopan', 'Tehuacán - Oaxaca', 'Puebla', 'Esperanza - Amozoc', 'Paseo de la República', 'Esperanza - Amozoc', 'Querétaro - Celaya', 'Manzana 023, Xala, Méx.', 'Esperanza - Fortin', 'Sagitario, Ecatepec de Morelos, Méx.', 'El Pedregal, Hidalgo', 'La Palma, Estado de México', 'Santo Domingo Aztacameca, Estado de México', 'Esperanza - Amozoc', 'Vista hermosa - Ecuandureo', 'San Luis - Lagos de Moreno', 'Lib. Sur 2, Texcacoa, Cuautitlán Izcalli, Méx.', 'Jorobas - Tula', 'P.º del Albatros, Santa Teresa,', 'Guadalajara - Atlacomulco', 'Lazaro Cardenas', 'Jorobas - Tula', 'La Tinaja - Acayucan', 'Guadalajara - Morelia', 'Cordoba- Puebla', 'Esperanza - Amozoc', 'Centro Gustavo Diaz Ordaz', 'Minatitlán - Córdoba', 'Esperanza - Amozoc', 'San Marcos - San Martin', 'Autopista Arco Norte salida a Tlaxcala', 'Autopista México - Puebla', 'Autopista Puebla - Tlaxcala', 'Km 33 carretera Guadalajara - Tepic', 'Carretera Jorobas, San Juan, Coyotepec', 'Tamuín, 79220 S.L.P.', 'Hueypoxtla, 55676 Méx.', 'Jorobas - Tula', 'Querétaro - Palmillas', 'Carretera Jorobas, San Juan, Coyotepec', 'Chichimequillas - SLP', 'Autopista México - Puebla', 'Chichimequillas - SLP', 'Calpulalpan, Tlaxcala', 'Carretera Zacatecas - San Luis Potosí', 'Xalapa - Puebla', 'Circuito Exterior Mexiquense', 'Benito Jurez el Moral', 'Carretera a la Jaulilla', 'Circuito Exterior Mexiquense', 'Av. José López Portillo 133, San Pedro Barrientos, Tlalnepantla de Baz, Méx.', 'Toluca - Naucalpan', 'Lorenzo Boturini 272, Esperanza, Cuauhtémoc, Ciudad de México, CDMX', 'Carretera Panamericana Zacatecas', 'León - Salamanca', 'Sayula de Aleman  Tierra Blanca', 'Calle Miguel Hidalgo', 'Circuito Exterior Mexiquense km 14', 'Amozoc De Mota - Nogales 119', 'Aculco', 'Guadalajara - Tepic ', 'Iguala - Cuernavaca', 'México - Pachuca', 'Circuito Exterior Mexiquense', 'Celaya - Salamanca ', 'Querétaro - Cerro gordo', 'Villagrán - Cortázar', 'Matehuala - San Luis Potosí']
estatusv = ['NO APLICA', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'CONSUMADO', 'CONSUMADO', 'RECUPERADO', 'RECUPERADO', 'CONSUMADO', 'RECUPERADO', 'RECUPERADO', 'CONSUMADO', 'CONSUMADO', 'NO APLICA', 'NO APLICA', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'CONSUMADO', 'CONSUMADO', 'CONSUMADO', 'RECUPERADO', 'CONSUMADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'CONSUMADO', 'CONSUMADO', 'RECUPERADO', 'RECUPERADO', 'CONSUMADO', 'PENDIENTE', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'CONSUMADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'CONSUMADO', 'RECUPERADO', 'CONSUMADO', 'CONSUMADO', 'FRUSTRADO', 'CONSUMADO', 'FRUSTRADO', 'FRUSTRADO', 'RECUPERADO', 'CONSUMADO', 'RECUPERADO', 'CONSUMADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'CONSUMADO', 'CONSUMADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO', 'RECUPERADO']
comentarios = ['No visible en Power Bi /Checklist de unidades', 'No visible en Power Bi /Checklist de unidades', 'No visible en Power Bi /Checklist de unidades', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'No visible en Power Bi', 'No visible en Power Bi', 'No visible en Power Bi', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'No visible en Power Bi /Checklist de unidades', 'No visible en Power Bi /Checklist de unidades', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Por indicaciones de Marcia no se va a contemplar (hasta que nos notifique cómo está la situación sobre las recuperaciones con Sitrack)', 'La unidad no sevisualiza dada dealta en PBI de AINSURENCE', 'La unidad no sevisualiza dada dealta en PBI de AINSURENCE', 'Sin observaciones', 'Sin observaciones', 'DENTRO DE LA PRUEBA / SI SE VISUALIZA EN EL 6TO ENVIO', 'DENTRO DE LA PRUEBA / SI SE VISUALIZA EN EL 6TO ENVIO / SE RECIBE ALERTA DE  DETECCIÓN DE INHIBICIÓN CELULAR', 'DENTRO DE LA PRUEBA / SI SE VISUALIZA EN EL 6TO ENVIO CON LAS PLACAS MAS516449', 'UNIDAD CON SERVICIO CARGADO A CLIENTE BASF / NO SE VISUALIZA EN EL 6TO ENVIO', 'SI SE VISUALIZA EN EL 6TO ENVIO', 'SI SE VISUALIZA EN EL 6TO ENVIO', 'SI SE VISUALIZA EN EL 6TO ENVIO', 'Con el VIM proporcionado se visualiza la unidad con placas 69AY5N posteriomente sitrack informa que el cliente se equivoca de placas, siendo las reales 75AY5M, posteriormente las vuelva a corroborar siendo correctas las placas 79AY5M', 'SITRACK NO REPORTA EL ROBO, SE DETECTA MEDIANTE ALERTA DE ROBO CONFIRMADO EN TELEGRAM', 'SITRACK NO REPORTA EL ROBO, SE DETECTA MEDIANTE ALERTA DE POSICIONAMIENTO Y RIESGO. SE DETECTA QUE ES UN ROBO YA QUE AL ARRIBAR AI27 NO LOCALIZAN EL TRACTO EN LA ÚLTIMA UBICACIÓN', 'SITRACK NO REPORTA LA RELEVANCIA, SE DETECTA ALERTA DE ROBO CONFIRMADO Y SE CONFIRMA EL PERCANCE CON EL ARRIBO DE GR Y GN, SITRACK INFORMA QUE SU ASEGURADORA SE HARÁ CARGO', 'UNIDAD CON SERVICIO CARGADO A CLIENTE COLGATE', 'Sin observaciones', '1 Hora con 35 minutos para notificar el robo del transporte.', 'Sin observaciones', '1 Hora con 23 minutos para notificar el robo del transporte.', 'Unidad con servicio AI27', 'Unidad cargada con servicio de AI27', 'Unidad cargada con servicio de AI27', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Unidad cargada con servicio de AI27', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', 'Sin observaciones', '9 horas de desfase entre la hora del robo y el reporte', 'Sin observaciones', 'Sin esquema de monitoreo', 'Sin observaciones', 'Sin observaciones']

for (fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment) in zip(fechas, names, bitacoras, clientes, entradas, marcas, modelos, placas, economicos, latitudes, longitudes, estados, municipios, tramos, estatusv, comentarios):
    ainsurance_db.insert_register_ainsurance(fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)