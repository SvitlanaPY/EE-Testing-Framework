"""sent_productID, sent_typeId, target_zipCode, target_storeId, target_materialId, target_materialName, target_colorId, target_productQteGrpId, retailer"""

EPM_DATA_toREPLACE = [
    (7957, 1102, 9029, "47025", 21885, 2524, "Laminate-Product Only", 8550, "Custom Amber Kashmire 6227-58", 787, 'lowes'),
    (8779, 1102, 8428, "47025", 21885, 2524, "Laminate-Product Only", 8550, "Custom Amber Kashmire 6227-58", 787, 'lowes'),
    (8780, 1102, 8431, "47025", 21885, 2524, "Laminate-Product Only", 8550, "Custom Amber Kashmire 6227-58", 787, 'lowes'),
    (8781, 1102, 8429, "47025", 21885, 2524, "Laminate-Product Only", 8550, "Custom Amber Kashmire 6227-58", 787, 'lowes'),
    (8680, 1102, 8447, "47025", 21885, 2524, "Laminate-Product Only", 8550, "Custom Amber Kashmire 6227-58", 787, 'lowes'),
    (7957, 1102, 9029, "47025", 21885, 2524, "Laminate-Product Only", 8890, "Fd Custom Autumn Carnival 1877k-35", 787, 'lowes'),
    (7958, 1102, 8427, "47025", 21885, 2524, "Laminate-Product Only", 8890, "Fd Custom Autumn Carnival 1877k-35", 787, 'lowes'),
    (8680, 1102, 8447, "47025", 21885, 2524, "Laminate-Product Only", 8890, "Fd Custom Autumn Carnival 1877k-35", 787, 'lowes'),
    (7957, 1102, 7957, "47025", 21885, 2520, "Laminate-Installed", 8740, "Midnight Stone 6280-46", 784, 'lowes'),
    (8778, 1102, 8778, "47025", 21885, 2520, "Laminate-Installed", 8740, "Midnight Stone 6280-46", 784, 'lowes'),
    (8779, 1102, 8779, "47025", 21885, 2520, "Laminate-Installed", 8740, "Midnight Stone 6280-46", 784, 'lowes'),
    (8780, 1102, 8780, "47025", 21885, 2520, "Laminate-Installed", 8740, "Midnight Stone 6280-46", 784, 'lowes'),
    (8781, 1102, 8781, "47025", 21885, 2520, "Laminate-Installed", 8740, "Midnight Stone 6280-46", 784, 'lowes'),
    (7957, 1102, 7957, "47025", 21885, 2520, "Laminate-Installed", 23085, "Toffee di Pesco 5000K-22", 784, 'lowes'),
    (7958, 1102, 7958, "47025", 21885, 2520, "Laminate-Installed", 23085, "Toffee di Pesco 5000K-22", 784, 'lowes'),
    (8680, 1102, 8680, "47025", 21885, 2520, "Laminate-Installed", 23085, "Toffee di Pesco 5000K-22", 784, 'lowes'),
    (8447, 1102, 8447, "47025", 21885, 2524, "Laminate-Product Only", 8557, "Custom Earthen Warp 5880-58", 787, 'lowes'),
    (9029, 1102, 9029, "47025", 21885, 2524, "Laminate-Product Only", 8557, "Custom Earthen Warp 5880-58", 787, 'lowes'),
    (8428, 1102, 8428, "47025", 21885, 2524, "Laminate-Product Only", 8557, "Custom Earthen Warp 5880-58", 787, 'lowes'),
    (8429, 1102, 8429, "47025", 21885, 2524, "Laminate-Product Only", 8557, "Custom Earthen Warp 5880-58", 787, 'lowes'),
    (8431, 1102, 8431, "47025", 21885, 2524, "Laminate-Product Only", 8557, "Custom Earthen Warp 5880-58", 787, 'lowes'),
    (8427, 1102, 8427, "47025", 21885, 2524, "Laminate-Product Only", 8557, "Custom Earthen Warp 5880-58", 787, 'lowes')
    ]

EPM_DATA_toREMOVE = [
    (7958, 1102, "47025", 21885, 2524, "Laminate-Product Only", 8550, "Custom Amber Kashmire 6227-58", 787, 'lowes'),
    (8778, 1102, "47025", 21885, 2524, "Laminate-Product Only", 8550, "Custom Amber Kashmire 6227-58", 787, 'lowes'),
    (8781, 1102, "47025", 21885, 2524, "Laminate-Product Only", 8890, "Fd Custom Autumn Carnival 1877k-35", 787, 'lowes'),
    (8779, 1102, "47025", 21885, 2524, "Laminate-Product Only", 8890, "Fd Custom Autumn Carnival 1877k-35", 787, 'lowes'),
    (8778, 1102, "47025", 21885, 2524, "Laminate-Product Only", 8890, "Fd Custom Autumn Carnival 1877k-35", 787, 'lowes'),
    (8780, 1102, "47025", 21885, 2524, "Laminate-Product Only", 8890, "Fd Custom Autumn Carnival 1877k-35", 787, 'lowes'),
    (8958, 1102, "47025", 21885, 2520, "Laminate-Installed", 8740, "Midnight Stone 6280-46", 784, 'lowes'),
    (8680, 1102, "47025", 21885, 2520, "Laminate-Installed", 8740, "Midnight Stone 6280-46", 784, 'lowes'),
    (8778, 1102, "47025", 21885, 2520, "Laminate-Installed", 23085, "Toffee di Pesco 5000K-22", 784, 'lowes'),
    (8779, 1102, "47025", 21885, 2520, "Laminate-Installed", 23085, "Toffee di Pesco 5000K-22", 784, 'lowes'),
    (8780, 1102, "47025", 21885, 2520, "Laminate-Installed", 23085, "Toffee di Pesco 5000K-22", 784, 'lowes'),
    (8781, 1102, "47025", 21885, 2520, "Laminate-Installed", 23085, "Toffee di Pesco 5000K-22", 784, 'lowes')
]
