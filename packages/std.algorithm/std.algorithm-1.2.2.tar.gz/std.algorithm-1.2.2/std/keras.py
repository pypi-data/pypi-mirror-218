from std import computed
import datetime, std, random, time
import numpy as np, regex as re
from std.data import numpify

from _collections import defaultdict
from types import FunctionType, MethodType
import inspect
import traceback

def is_torch(model):
    # Method Resolution Order by C3 Linearization algorithm
    return any(str(t) == "<class 'torch.nn.modules.module.Module'>" for t in reversed(type(model).__mro__))

def availableGPU():
# pip install nvidia-ml-py3
    try:
        import pynvml  # @UnresolvedImport
        pynvml.nvmlInit()
    except Exception as e:
        print(e)
        traceback.print_exc()
        return -1
#         shutil.copy('C:/Windows/System32/nvml.dll', 'C:/Program Files/NVIDIA Corporation/NVSMI/nvml.dll')
    # fix: copy C:\Windows\System32\nvml.dll and paste to C:\Program Files\NVIDIA Corporation\NVSMI\nvml.dll

    maxFreeMemory = 0
    maxFreeMemoryID = 0
    for i in range(pynvml.nvmlDeviceGetCount()):
        print('the %dth GPU info:' % i)
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        print('used memory = ', meminfo.used / (1 << 20))
        print('free memory = ', meminfo.free / (1 << 20))
        print('total memory = ', meminfo.total / (1 << 20))
        if meminfo.free > maxFreeMemory:
            maxFreeMemoryID = i
            maxFreeMemory = meminfo.free

    print('GPU with the maximum Free Memory is %d, with Free Memory of %f MiB' % (maxFreeMemoryID, maxFreeMemory / (1 << 20)))
    
    ids = {maxFreeMemoryID}
    for i in range(pynvml.nvmlDeviceGetCount()):
        if i == maxFreeMemoryID:
            continue
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)        
        print('meminfo.free =', meminfo.free)
        print('maxFreeMemory * 0.9 =', maxFreeMemory * 0.9)
        if meminfo.free > maxFreeMemory * 0.999999:
            ids.add(i)
    
    print('ids =', ids)
    device_id = [*ids][random.randrange(0, len(ids))]
    print('selected device_id =', device_id)
    import os
    gpu_count = os.environ.get('gpu_count')
    if gpu_count:
        ...
        
    return device_id

def initialize_vocab(file, start=2):
    index = start
    vocab = {}
    from std.file import Text
    for word in Text(file):
        assert word and word == word.strip()
        assert word not in vocab
        vocab[word] = index
        index += 1
    return vocab

def method_name(func): 
    if inspect.ismethod(func):
        self = func.__self__
        if hasattr(self, 'name'):
            name = self.name
        else:
            name = self.__class__.__name__
        
        return name + '.' + func.__func__.__name__
    
    if inspect.isfunction(func):
        return func.__qualname__
    
    return func.__qualname__

def print_decimal(avg):
    if abs(avg) > 1e-3:
        return '%.4f' % avg
    else:
        return '%.4e' % avg
           
def print_time(eta):
    if eta > 3600:
        return '%d:%02d:%02d' % (eta // 3600, (eta % 3600) // 60, eta % 60)
    elif eta > 60:
        return '%d:%02d' % (eta // 60, eta % 60)
    else:
        return '%ds' % eta

class SymbolicModel:
    
    def __init__(self, model=None):
        self.model = model
    
    def sanctity_check(self):
        if self.vocab:
            assert min(self.vocab.values()) == 2
            assert max(self.vocab.values()) == self.dimension - 1
        return True
        
    def initialize_vocab(self, start=2):
        self.vocab = initialize_vocab(self.vocabFile, start=start)
        self.sanctity_check()
        self.UNK_INDEX = 1
        
    @property
    def dimension(self):
        return len(self.vocab) + 2

    def string2id(self, s):
        assert len(s) > 0
        return [self.vocab.get(i, self.UNK_INDEX) for i in s]

    def string2ids(self, s):
        return [[self.vocab.get(c, self.UNK_INDEX) for c in w] for w in s]
        
    def preprocess(self):
        self.model.outputs
        self.model.make_substitutions()
        
    def state_dict(self, modelPath):
        print('loading', modelPath)
        import h5py
        with h5py.File(modelPath, mode='r') as f:
            return self.model.load_weights(f)

    def __call__(self, *inputs, **kwargs):
        with self.context(**kwargs):
            return self.forward(*inputs)
        
    def forward(self, *inputs):
        for symbol, data in zip(self.model.inputs, inputs):
            symbol.numpy = data
            for symbolic_size, size in zip(symbol.shape, data.shape):
                symbolic_size.numpy = np.array(size)
        
        outputs = self.model.outputs
        
        if isinstance(outputs, (tuple, list)):
            data = type(outputs)((type(output)(output.torch for output in output) if isinstance(output, (tuple, list)) else output.torch for output in outputs))
        else:
            data = outputs.torch
            
        return data


class KerasModel: 

    numpify_x = numpify
    device = 0
    learning_rate = 5e-5
    
    @staticmethod
    def is_integer(data):
        if isinstance(data, (tuple, list)):
            return all(KerasModel.is_integer(d) for d in data)
        return isinstance(data, int)
    
    @staticmethod
    def numpify_y(arr):
        if KerasModel.is_integer(arr):
            return numpify(arr, mask_value=-1, dtype=np.int64)
        return numpify(arr)

    def __init__(self, **kwargs):
        self.lang = kwargs.pop('lang', None)
        
        if hasattr(self, 'model'):
            if self.is_torch:
                self.model.eval()
                import torch
                if torch.cuda.is_available():
                    self.model.to(0)
                    self.device = 0
                    return

        self.device = -1

    def replace_vocab(self, vocab, limit):

        def replace_vocab(vocab):
            deletes = set()
            existentKeys = set()
            for key, index in self.vocab.items():
                if key in vocab:
                    existentKeys.add(key)
                else:
                    deletes.add(key)
            vocab -= existentKeys
            vocab = [*vocab]
            assert len(vocab) >= len(deletes)
            for key in deletes:
                index = self.vocab[key]
                       
                self.vocab[vocab.pop()] = index
                del self.vocab[key]
            return {*vocab}
            
        if isinstance(vocab, dict):
            vocab = [*vocab.items()]
            vocab.sort(key=lambda pair: pair[1], reverse=True)
            vocab = vocab[:limit]
            vocab = {word for word, _ in vocab}
    
        if len(vocab) >= len(self.vocab):
            vocab = replace_vocab(vocab)
            print('calling self.expand_vocabulary(vocab)')           
            self.expand_vocabulary(vocab)
        else:
            print('calling self.shrink_vocabulary(vocab)')
            self.shrink_vocabulary(vocab)
            replace_vocab(vocab)            
        
    def shrink_vocabulary(self, charSet):
        if len(charSet) >= len(self.vocab):
            return
        
        numOfDeletes = len(self.vocab) - len(charSet)
# delete key with the index of :         
#         len(self.vocab) + 1, len(self.vocab), len(self.vocab) - 1, len(self.vocab) - numOfDeletes + 2
        deletes = set()
        for key, index in self.vocab.items():
            if index >= len(self.vocab) - numOfDeletes + 2:
                deletes.add(key)
                
        for key in deletes:
            del self.vocab[key]
        
        for embeddingLayer in self.model.modules():
            if isinstance(embeddingLayer, nn.Embedding):
                weight = embeddingLayer.weight
                break
                
        vocab_size, embed_size = weight.shape
        _weight = weight[:vocab_size - numOfDeletes]
        del self.model
        self.create_model()
        
        for embeddingLayer in self.model.modules():
            if isinstance(embeddingLayer, nn.Embedding):
                weight = embeddingLayer.weight
                break
           
        with torch.no_grad():
            weight[:] = _weight
        
    def expand_vocabulary(self, charSet):
        charSet -= self.vocab.keys()
        if not charSet:
            return
        
        print('%d new words found!' % len(charSet))
    
        index = self.dimension
        self.vocab.update({word: i + index for i, word in enumerate(charSet)})
        weights = self.model.get_weights()
#         weights = self.model.layers[1].get_weights()
                
        shape = weights[0].shape
        dimensionAdded = self.dimension - shape[0]
        assert dimensionAdded > 0

        weights[0] = np.append(weights[0], np.random.normal(0, 0.01, (dimensionAdded, shape[1])), 0)

        del self.model
        print('recreating model')
        self.create_model()
        self.model.set_weights(weights)
        
    def initialize_vocab(self, start=2):
        self.vocab = initialize_vocab(self.vocabFile, start=start)
        self.sanctity_check()
        self.UNK_INDEX = 1

    def sanctity_check(self):
        if self.vocab:
            assert min(self.vocab.values()) == 2
            assert max(self.vocab.values()) == self.dimension - 1
        return True

    def update_vocab(self):
        if not hasattr(self, 'vocab'):
            return
        
        self.sanctity_check()
        
        array = [None] * len(self.vocab)
        for word, index in self.vocab.items():
            array[index - 2] = word
        
        print('saving vocab to', self.vocabFile)
        with open(self.vocabFile, 'w', encoding='utf8') as file:
            for word in array:
                assert word and word == word.strip(), "word =" + word
                print(word, file=file, end='\n')

    def print_history(self, history, delimiter='\n'):
        length = len(history['loss'])
        
        arr = []
        for i in range(length):
            dic = {}
            for key, value in history.items():
                dic[key] = value[i]
            arr.append(str(dic))
        
        print(delimiter.join(arr))   
        print("printed at", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 

    @property
    def dimension(self):
        return len(self.vocab) + 2

    def string2id(self, s):
        assert len(s) > 0
        return [self.vocab.get(i, self.UNK_INDEX) for i in s]

    @computed
    def metrics(self):
        if hasattr(self, 'loss'):
            loss = self.loss
            accuracy = self.accuracy
        else:
            output_layer = [layer for layer in self.model.layers if hasattr(layer, 'loss')]
            if not output_layer:
                output_layer = self.model
            elif len(output_layer) == 1:
                output_layer, = output_layer
                
            if isinstance(output_layer, list):
                loss = [layer.loss for layer in output_layer]
                accuracy = [layer.accuracy for layer in output_layer]
            else:
                loss = output_layer.loss
                accuracy = output_layer.accuracy
            
        return dict(loss=loss, accuracy=accuracy)
    
    @property
    def loss(self):
        return self.metrics['loss']
    
    @property
    def accuracy(self):
        return self.metrics['accuracy']
            
    def forward(self, x):
        return self.model.forward(x)

    @std.Timer('training')
    def training(self, **kwargs):
        epochs = kwargs.pop('epochs', None) or getattr(self, 'epochs', 2)
        print('epochs =', epochs)
        
        batch_size = kwargs.pop('batch_size', None) or getattr(self, 'batch_size', 64)
        print('batch_size =', batch_size)
        
        training = kwargs.pop('training', 1)
        print('training =', training)
        
        device = self.device
        print("device =", device)

        learning_rate = kwargs.pop('learning_rate', None) or getattr(self, 'learning_rate', 5e-5)
        print("learning_rate =", learning_rate)
        
        dynamic_size = kwargs.pop('dynamic_size', None) or getattr(self, 'dynamic_size', None)
        print("dynamic_size =", dynamic_size)

        args = {}
        if self.is_torch:
            args['torch'] = True
        else:
            args['keras'] = True

        generator = Sequence(self.load_data(training, **kwargs),
                             batch_size=batch_size,
                             dynamic_size=dynamic_size,
                             numpify_x=self.numpify_x,
                             numpify_y=self.numpify_y, **args)
        
        if self.is_torch:
            if hasattr(self, 'optimizer'):
                optimizer = self.optimizer
            else:                
                optimizer = AdamW(self.model.parameters(), learning_rate)
                self.optimizer = optimizer
                
            if hasattr(self, 'scheduler'):
                scheduler = self.scheduler(len(generator), epochs=epochs)
            else:
                scheduler = get_polynomial_decay_schedule_with_warmup(optimizer, len(generator) * epochs)
            optimizer.scheduler = scheduler
            
        else:
            optimizer = AdamW(WarmupPolynomialDecay(learning_rate, len(generator) * epochs))
            self.optimizer = optimizer

        def on_epoch_end(*_):
            self.save_weights()
            self.update_vocab()
        
        history = self.fit_generator(generator,
                           epochs=epochs,
                           callbacks=LambdaCallback(on_epoch_end=on_epoch_end))
        
        self.print_history(history)

    def fit_generator(self,
            train_data,
            val_data=[],
            epochs=10,
            patience=5,
            monitor="val_loss",
            mode="min", 
            callbacks=[],
            shuffle=True):
        if not isinstance(callbacks, list):
            callbacks = [callbacks]
            
        history = {}
        for epoch in range(epochs):
            print("Epoch {0}/{1}\n".format(epoch + 1, epochs))

            if shuffle:
                train_data.shuffle()
            
            train_step_runner = StepRunner(
                model=self.model,
                training=True,
                optimizer=self.optimizer,
                device=self.device,
                **self.metrics)
            
            train_metrics = EpochRunner(train_step_runner)(train_data)
            for callback in callbacks:
                callback.on_epoch_end()
                
            for name, metric in train_metrics.items():
                history[name] = history.get(name, []) + [metric]

            if val_data:
                val_step_runner = StepRunner(
                    model=self.model,
                    training=False,
                    device=self.device,
                    **self.metrics)
                
                val_epoch_runner = EpochRunner(val_step_runner)
                
                with torch.no_grad():
                    val_metrics = val_epoch_runner(val_data)
                    
                val_metrics["epoch"] = epoch
                for name, metric in val_metrics.items():
                    self.history[name] = self.history.get(name, []) + [metric]
            
            # early-stopping -------------------------------------------------
            if not val_data:
                continue
            
            arr_scores = history[monitor]
            best_score_idx = np.argmax(arr_scores) if mode == "max" else np.argmin(arr_scores)
            if best_score_idx == len(arr_scores) - 1:
                print("<<<<<< reach best {0} : {1} >>>>>>".format(monitor, arr_scores[best_score_idx]), file=sys.stderr)
            if len(arr_scores) - best_score_idx > patience:
                print("<<<<<< {} without improvement in {} epoch, early stopping >>>>>>".format(monitor, patience), file=sys.stderr)
                break
 
        return history

    @std.Timer('evaluate')
    def evaluate(self, **kwargs):
        batch_size = kwargs.pop('batch_size', None) or getattr(self, 'batch_size', 64)
        print('batch_size =', batch_size)
        
        training = kwargs.pop('training', 0)
        print('training =', training)
        
        device = self.device
        print("device =", device)

        args = {}
        if self.is_torch:
            args['torch'] = True
        else:
            args['keras'] = True

        generator = Sequence(self.load_data(training, **kwargs),
                             batch_size=batch_size,
                             numpify_x=self.numpify_x,
                             numpify_y=self.numpify_y, **args)
        
        return EpochRunner(
            StepRunner(
                model=self.model, 
                training=False,
                device=self.device, 
                **self.metrics))(generator)

    @std.Timer('predict')
    def predict(self, inputs, **kwargs):
        batch_size = kwargs.pop('batch_size', len(inputs))
        
        device = self.device

        args = {}
        if self.is_torch:
            args['torch'] = True
        else:
            args['keras'] = True

        args['sort'] = kwargs.get('sort', False)
        generator = Sequence(inputs,
                             batch_size=batch_size,
                             numpify_x=self.numpify_x,
                             numpify_y=self.numpify_y, **args)
        
        return EpochRunner(
            StepRunner(
                model=self.model, 
                training=False,
                device=self.device)).predict(generator)

    def load_weights(self):
        print('\nloading model from', self.modelFile)
        import h5py
        with h5py.File(self.modelFile, 'r') as f:
            self.iostream(self.model, f, mode='r')
            
    @property
    def iostream(self):
        if self.backend == 'keras':
            from .tensorflow.hdf5 import iostream
        elif self.backend == 'torch':
            from .torch.hdf5 import iostream
            import torch
            iostream = torch.no_grad()(iostream)
        return iostream
        
    def save_weights(self):
        modelFile = self.modelFile
        print('\nsaving model to', modelFile)
        import os
        from std.file import createNewPath
        createNewPath(os.path.dirname(modelFile))

        if modelFile.endswith('.h5'):
            import h5py
            with h5py.File(modelFile, 'w') as f:
                self.iostream(self.model, f, mode='w')

        elif modelFile.endswith('.pt'):
            import torch
            torch.save(self.model, modelFile)

        elif modelFile.endswith('.bin'):
            import torch
            torch.save(self.model.state_dict(), modelFile)
                
    @computed
    def is_torch(self):
        return is_torch(self.model)


def get_tensor_shape(tensor, axis=None):
    if axis is None:
        shape = []
        while isinstance(tensor, (list, tuple)):
            shape.append(len(tensor))    
            tensor = tensor[0]
            
        return shape

    else:
        for i in range(axis):
            tensor = tensor[0]
        return len(tensor)


class Sequence:

    def __init__(self,
                 original_list,
                 x_name=None,
                 y_name=None,
                 batch_size=32,
                 dynamic_size=None,
                 shuffle=False,
                 numpify_x=None,
                 numpify_y=None,
                 sort=True,
                 reverse=False,
                 **kwargs):
        
        if dynamic_size:
            if isinstance(dynamic_size, (FunctionType, MethodType)):
                self.batch_size = batch_size
                self.dynamic_size = dynamic_size
            else:
                self.batch_size = dynamic_size
                self.dynamic_size = True
        else:
            self.batch_size = batch_size
            self.dynamic_size = False
            
        from inspect import isgenerator
        if isgenerator(original_list):
            original_list = [*original_list]
            
        if x_name is None:
            try:
                doc = original_list[0].__doc__.strip()
                args = eval(doc)
            except SyntaxError:
                args = [re.split('\s*:\s*', declspec)[0] for declspec in re.split('\s*,\s*', re.match('\w+\((.+)\)$', doc)[1])]
            
            *x_name, y_name = args
            if len(x_name) == 1:
                x_name = x_name[0]
        
        self.x_name = x_name
        if sort:
            self.original_list = original_list
            self.counting_sort(reverse=reverse)
        else:
            self.training_list = original_list

        self.y_name = y_name
        self.numpify_x = numpify_x
        self.numpify_y = numpify_y if y_name else None
        
        if kwargs:
            self.backend, = kwargs
        else:
            self.backend = 'keras'
            
        self.arr = [self.to_tensor(batch) for batch in self.batches()]
        
        if shuffle if y_name else False:
            self.shuffle(self.arr)
        
    def predict(self, model, numpy=True): 
        return self.reorder(model.predict_generator(self), numpy=numpy)
    
    def reorder(self, y_pred, numpy=True):
        if not hasattr(self, 'original_list'):
            return y_pred
        
        for inst, result in zip(self.training_list, y_pred):
            inst.result = result
        y_pred = [inst.result for inst in self.original_list]
        
        if numpy:
            y_pred = np.array(y_pred)           
        return y_pred
        
    def counting_sort(self, reverse=False):
        if isinstance(self.x_name, str):
            self.training_list = counting_sort(self.original_list, self.x_name, reverse=reverse)
        else:
            training_list = self.original_list
            for x_name in self.x_name:
                training_list = counting_sort(training_list, x_name, reverse=reverse)
            self.training_list = training_list
        
    def __getitem__(self, index):
        return self.arr[index]
    
    def get_memory_allocation(self, tensor):
        shape = get_tensor_shape(tensor)
        if isinstance(self.dynamic_size, (FunctionType, MethodType)):
            return self.dynamic_size(*shape)

        from _functools import reduce
        return reduce(lambda x, y: x * y, shape)
        
    def batches(self): 
        if self.dynamic_size:
            if isinstance(self.x_name, str):
                x_name = self.x_name
            else:
                x_name = self.x_name[0]
                
            memorySize = 0
            for inst in self.training_list:
                memorySize += self.get_memory_allocation(getattr(inst, x_name))

            memorySize /= len(self.training_list)
            batch_memory = self.batch_size * memorySize
            
            batch_size = self.batch_size
            _memorySize = self.get_memory_allocation(getattr(self.training_list[batch_size - 1], x_name))
            if _memorySize < memorySize:
                _batch_size = max(1, int(batch_memory / _memorySize))
                if _batch_size > batch_size:
                    batch_size = _batch_size
                    memorySize = _memorySize
                    print('initial batch_size =', batch_size)

            i = 0
            while i < len(self.training_list):
                _memorySize = self.get_memory_allocation(getattr(self.training_list[i + batch_size - 1], x_name))
                if _memorySize > memorySize:
                    _batch_size = max(1, int(batch_memory / _memorySize))
                    if _batch_size < batch_size:
                        batch_size = _batch_size
                        memorySize = _memorySize
                        print('adjust batch_size to', batch_size)
     
                yield self.training_list[i:i + batch_size]
                i += batch_size
        else: 
            for i in range(0, len(self.training_list), self.batch_size):
                yield self.training_list[i:i + self.batch_size]

    def shuffle(self):
        # print("shuffling the data")
        random.shuffle(self.arr)
        
    def __len__(self):
        return len(self.arr)

    def on_epoch_end(self):
        print('\none epoch has ended!')

    @staticmethod
    def format_sample(batch, attribute, format_func):
        sample = [getattr(s, attribute) for s in batch]
            
        batch = format_func(sample) if format_func else np.array(sample)
        if batch.dtype == object:
            return numpify(sample)
        return batch

    @staticmethod
    def format_data(batch, attributes, format_func):
        if isinstance(attributes, (list, tuple)):
            samples = []
            if isinstance(format_func, (list, tuple)):
                for attribute, format_func in zip(attributes, format_func):
                    samples.append(Sequence.format_sample(batch, attribute, format_func))
            else:
                for attribute in attributes:
                    samples.append(Sequence.format_sample(batch, attribute, format_func))
            return samples
        elif attributes:
            return Sequence.format_sample(batch, attributes, format_func)

    def to_tensor(self, batch):
        args = self.numpify(batch)
        if isinstance(args, tuple):
            return tuple([self.from_numpy(arg) for arg in arg] if isinstance(arg, list) else self.from_numpy(arg) for arg in args)
        
        if isinstance(args, list):
            return tuple(self.from_numpy(arg) for arg in args)
        
        return self.from_numpy(args)
                
    def numpify(self, batch):
        assert batch is not None

        x_sample = self.format_data(batch, self.x_name, self.numpify_x)

        if self.y_name:
            y_sample = self.format_data(batch, self.y_name, self.numpify_y)
            return x_sample, y_sample
        return x_sample

    def from_numpy(self, ndarray):
        if self.backend == 'keras':
            import tensorflow as tf
            return tf.constant(ndarray)
        
        if self.backend == 'torch':
            import torch
            return torch.from_numpy(ndarray)

def counting_sort(original_list, attr, reverse=False, axis=0):
    training_list = []
    dicOfInstance = []    
            
    for inst in original_list:
        tensor = getattr(inst, attr)
        seq_length = get_tensor_shape(tensor, axis)
        assert seq_length > 0
        
        if len(dicOfInstance) < seq_length:
            dicOfInstance += [None] * (seq_length - len(dicOfInstance))
            
        index = seq_length - 1
        
        if dicOfInstance[index] is None:
            dicOfInstance[index] = []
        
        dicOfInstance[index].append(inst)
        
    # concatenate all the instances order by seq_length
    # print('maximum seq_length =', len(dicOfInstance))
    
    for index in range(len(dicOfInstance)):
        if dicOfInstance[index] is not None:
            batches = dicOfInstance[index]
            if axis + 1 < len(get_tensor_shape(getattr(batches[0], attr))):
                batches = counting_sort(batches, attr, reverse=False, axis=axis + 1)
            training_list += batches
            
    if reverse:
        training_list.reverse()
        
    return training_list
    

class Callback(object):
    """Abstract base class used to build new callbacks.
    """

    def __init__(self):
        self.validation_data = None
        self.model = None

    def set_params(self, params):
        self.params = params

    def set_model(self, model):
        self.model = model

    def on_batch_begin(self, batch, logs=None):
        """A backwards compatibility alias for `on_train_batch_begin`."""

    def on_batch_end(self, batch, logs=None):
        """A backwards compatibility alias for `on_train_batch_end`."""

    def on_epoch_begin(self, epoch, logs=None):
        """Called at the start of an epoch.
        """

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch.
        """

    def on_train_batch_begin(self, batch, logs=None):
        """Called at the beginning of a training batch in `fit` methods.
        """
        # For backwards compatibility
        self.on_batch_begin(batch, logs=logs)

    def on_train_batch_end(self, batch, logs=None):
        """Called at the end of a training batch in `fit` methods.
        """
        # For backwards compatibility
        self.on_batch_end(batch, logs=logs)

    def on_test_batch_begin(self, batch, logs=None):
        """Called at the beginning of a batch in `evaluate` methods.
        """

    def on_test_batch_end(self, batch, logs=None):
        """Called at the end of a batch in `evaluate` methods.
        """

    def on_predict_batch_begin(self, batch, logs=None):
        """Called at the beginning of a batch in `predict` methods.
        """

    def on_predict_batch_end(self, batch, logs=None):
        """Called at the end of a batch in `predict` methods.
        """

    def on_train_begin(self, logs=None):
        """Called at the beginning of training.
        """

    def on_train_end(self, logs=None):
        """Called at the end of training.
        """

    def on_test_begin(self, logs=None):
        """Called at the beginning of evaluation or validation.
        """

    def on_test_end(self, logs=None):
        """Called at the end of evaluation or validation.
        """

    def on_predict_begin(self, logs=None):
        """Called at the beginning of prediction.
        """

    def on_predict_end(self, logs=None):
        """Called at the end of prediction.
        """


class LambdaCallback(Callback):
    r"""
    Create a simple callback on the fly using lambda functions.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                setattr(self, k, v)


class EpochRunner:

    def __init__(self, steprunner):
        self.steprunner = steprunner
        if self.training:
            if self.is_torch:
                steprunner.model.train()
            else:
                steprunner.model.training = True
        else:
            if self.is_torch:
                steprunner.model.eval()
            else:
                steprunner.model.training = False
        
    width = 30
    
    def __call__(self, dataloader):
        
        total_loss = 0
        total_count = 0
        
        loss_dict = defaultdict(float)
        accuracy_dict = defaultdict(float)
        
        target = len(dataloader)
        total_time = 0
        
        if self.is_torch:
            import torch
        else:
            import tensorflow as tf
            
        for current, batch in enumerate(dataloader):
            if self.device >= 0: 
                if self.is_torch:
                    if isinstance(batch, tuple):
                        batch = [*batch]

                    for i, data in enumerate(batch):
                        if isinstance(data, (list, tuple)):
                            data = [data.to(self.device) for data in data]
                        else:
                            if data.dtype == torch.int:
                                data = data.long()
                            data = data.to(self.device)
                        batch[i] = data
                else:
                    ...

            time_start = time.time()

            current += 1
            if self.training:
                try:
                    loss_per_batch, loss_items, accuracy_items = self.steprunner(*batch)
                except tf.errors.InternalError as e:
                    print(e)
                    traceback.print_exc()
                    import sys
                    sys.exit()

                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    continue
            else:
                with torch.no_grad():
                    args = self.steprunner(*batch)
                    if self.steprunner.loss:
                        loss_per_batch, loss_items, accuracy_items = args
                    else:
                        return args
                   
            if self.is_torch:
                total_loss += loss_per_batch.sum().item()
                total_count += loss_per_batch.numel()
            
                for name, val in loss_items.items():
                    loss_dict[name] += val.sum().item()
                    
                for name, val in accuracy_items.items():
                    if val.dtype == torch.bool:
                        val = val.float()
                    accuracy_dict[name] += val.sum().item()
            else:
                total_loss += tf.reduce_sum(loss_per_batch).numpy()
                total_count += loss_per_batch._num_elements()
                
                for name, val in loss_items.items():
                    loss_dict[name] += tf.reduce_sum(val).numpy()
                    
                for name, val in accuracy_items.items():
                    if val.dtype is tf.bool:
                        val = tf.cast(val, tf.int32)
                    accuracy_dict[name] += tf.reduce_sum(val).numpy()

            history = dict(loss=total_loss / total_count)
            historyLoss = {name: value / total_count for name, value in loss_dict.items()}
            history.update(**historyLoss)
            
            historyAccuracy = {name: value / total_count for name, value in accuracy_dict.items()}
            history.update(**historyAccuracy)
            
            bar = '%%%dd/%d' % (int(np.floor(np.log10(target))) + 1, target) % current
            
            prog = float(current) / target
            prog_width = int(self.width * prog)
            
            progress_bar = ''
            if prog_width > 0:
                progress_bar += ('=' * (prog_width - 1))
                if current < target:
                    progress_bar += '>'
                else:
                    progress_bar += '='
                    
            progress_bar += '.' * (self.width - prog_width)
            
            strs = [f'{bar} [{progress_bar}]', '', f"loss: {print_decimal(history['loss'])}"]
            
            if len(historyLoss) > 1:
                strs += [f"{name}: {print_decimal(value)}" for name, value in historyLoss.items()]

            strs += [f"{name}: {print_decimal(value)}" for name, value in historyAccuracy.items()]
            
            total_time += time.time() - time_start
            ETA = (target - current) * total_time / current
            strs[1] = f'ETA: {print_time(ETA)}'
            print(' - '.join(strs))
            
        return history

    def predict(self, dataloader):
        
        if self.is_torch:
            import torch
        else:
            import tensorflow as tf
            
        history = []
        for current, batch in enumerate(dataloader):
            if self.device >= 0: 
                if self.is_torch:
                    if isinstance(batch, tuple):
                        batch = [*batch]

                    for i, data in enumerate(batch):
                        if isinstance(data, (list, tuple)):
                            data = [data.to(self.device) for data in data]
                        else:
                            if data.dtype == torch.int:
                                data = data.long()
                            data = data.to(self.device)
                        batch[i] = data
                else:
                    ...

            with torch.no_grad():
                args = self.steprunner(*batch)
                history.append(args)
                   
        return torch.vstack(history)

    @property
    def is_torch(self):
        return self.steprunner.is_torch

    @property
    def device(self):
        return self.steprunner.device
    
    @property
    def training(self):
        return self.steprunner.training


class StepRunner:

    def __init__(self, model, training=True, loss=None, accuracy=None, optimizer=None, accelerator=None, device=-1):
        self.model, self.loss, self.accuracy = model, loss, accuracy
        self.training = training
        self.optimizer = optimizer
        self.accelerator = accelerator
        self.device = device
    
    def __call__(self, features, y_true):
        if self.is_torch:
            import torch
            try:
                y_pred = self.model(*features) if isinstance(features, list) else self.model(features)
            except RuntimeError as e:
                if "out of memory" in str(e):
                    if hasattr(torch.cuda, 'empty_cache'):
                        torch.cuda.empty_cache()
                
                traceback.print_exc()
                raise e
            except Exception as e:
                traceback.print_exc()
                raise e
            
            if self.loss:
                if isinstance(self.loss, (list, tuple)):
                    loss_dict = {method_name(loss_fn): loss_fn(y_true, y_pred) for loss_fn, y_true, y_pred in zip(self.loss, y_true, y_pred)}
                else:
                    loss_dict = {method_name(self.loss): self.loss(y_true, y_pred)}
    
                loss = sum(loss_dict.values())
                # backward()
                if self.optimizer is not None and self.training:
                    loss_mean = torch.mean(loss)
                
                    if torch.isnan(loss_mean):
                        print(loss_mean + 'is nan, stop training')
                        raise Exception('nan error') 
                
                    if self.accelerator is None:
                        loss_mean.backward()
                    else:
                        self.accelerator.backward(loss_mean)
        
                    self.optimizer.step()
                    
                    try:
                        scheduler = self.optimizer.scheduler
                        if scheduler is not None:
                            scheduler.step()# Update learning rate schedule
                    except AttributeError:
                        ...
                        
                    self.optimizer.zero_grad()
            else:
                return y_pred
        else:
            import tensorflow as tf
            with tf.GradientTape() as tape:
                y_pred = self.model(*features) if isinstance(features, list) else self.model(features)
               
                if isinstance(self.loss, (list, tuple)):
                    loss_dict = {method_name(loss_fn): loss_fn(y_true, y_pred) for loss_fn, y_true, y_pred in zip(self.loss, y_true, y_pred)}
                else:
                    loss_dict = {method_name(self.loss): self.loss(y_true, y_pred)}
        
                loss = sum(loss_dict.values())
                # backward()
                if self.optimizer is not None and self.training:
                    loss_mean = tf.reduce_mean(loss)
                    
                    if self.accelerator is None:
                        trainable_variables = self.model.trainable_variables
                        self.optimizer.apply_gradients(zip(tape.gradient(loss_mean, trainable_variables), trainable_variables))
                    else:
                        ...
            
        if isinstance(self.accuracy, dict):
            step_metrics = {name: metric_fn(y_true, y_pred) for name, metric_fn in self.accuracy.items()}
        elif isinstance(self.accuracy, (list, tuple)):
            step_metrics = {method_name(metric_fn): metric_fn(y_true, y_pred) for metric_fn, y_true, y_pred in zip(self.accuracy, y_true, y_pred)}
        else:
            step_metrics = {method_name(self.accuracy): self.accuracy(y_true, y_pred)}
        
        return loss, loss_dict, step_metrics

    @computed
    def is_torch(self):
        return is_torch(self.model)
