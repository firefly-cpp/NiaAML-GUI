class ProcessWindowData:
    def __init__(
        self,
        isOptimization,
        csvSrc=None,
        csvHasHeader=None,
        encoder=None,
        imputer=None,
        optAlgName=None,
        optAlgInnerName=None,
        popSize=None,
        popSizeInner=None,
        numEvals=None,
        numEvalsInner=None,
        fsas=None,
        ftas=None,
        classifiers=None,
        fitnessFunctionName=None,
        outputFolder=None,
        pipelineSrc=None,
    ):
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
        
    @staticmethod
    def from_dict(d):
        return ProcessWindowData(
            isOptimization=d.get("isOptimization", False),
            csvSrc=d.get("csvSrc"),
            csvHasHeader=d.get("csvHasHeader"),
            encoder=d.get("Categorical Encoder", ""),
            imputer=d.get("Missing Imputer", ""),
            optAlgName=d.get("Optimization Algorithm (Selection)", ""),
            optAlgInnerName=d.get("Optimization Algorithm (Tuning)", ""),
            popSize=d.get("Population Size (Components Selection)", ""),
            popSizeInner=d.get("Population Size (Parameter Tuning)", ""),
            numEvals=d.get("Number of Evaluations (Component Selection)", ""),
            numEvalsInner=d.get("Number of Evaluations (Parameter Tuning)", ""),
            fsas=d.get("Feature Selection", ""),
            ftas=d.get("Feature Transform", ""),
            classifiers=d.get("Classifier", ""),
            fitnessFunctionName=d.get("Fitness Function", ""),
            outputFolder=d.get("Pipeline Output Folder", ""),
            pipelineSrc=d.get("pipelineSrc", "")
        )
        