class ProcessWindowData:
    def __init__(
        self,
        isOptimization,
        csvSrc = None,
        csvHasHeader = None,
        encoder = None,
        imputer = None,
        optAlgName = None,
        optAlgInnerName = None,
        popSize = None,
        popSizeInner = None,
        numEvals = None,
        numEvalsInner = None,
        fsas = None,
        ftas = None,
        classifiers = None,
        fitnessFunctionName = None,
        outputFolder = None,
        pipelineSrc = None):
        self.isOptimization = isOptimization
        self.csvSrc = csvSrc
        self.csvHasHeader = csvHasHeader
        self.encoder = encoder
        self.imputer = imputer
        self.optAlgName = optAlgName
        self.optAlgInnerName = optAlgInnerName
        self.popSize = popSize
        self.popSizeInner = popSizeInner
        self.numEvals = numEvals
        self.numEvalsInner = numEvalsInner
        self.fsas = fsas if fsas is not None and len(fsas) > 0 else None
        self.ftas = ftas if ftas is not None and len(ftas) > 0 else None
        self.classifiers = classifiers
        self.fitnessFunctionName = fitnessFunctionName
        self.outputFolder = outputFolder
        self.pipelineSrc = pipelineSrc