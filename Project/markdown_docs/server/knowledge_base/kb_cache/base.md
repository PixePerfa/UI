## ClassDef ThreadSafeObject
**ThreadSafeObject**: The function of the ThreadSafeObject class is to provide a thread-safe object encapsulation for safely accessing and modifying objects in a multithreaded environment. 

**Properties**:
- `_obj`: Stores the properties of the actual object, which can be of any type.
- `_key`: The key of an object that identifies the object and can be a string or tuple.
- `_pool`: The cache pool to which the object belongs, of type , `CachePool`defaults to None. 
- `_lock`: A reentrant lock(`threading.RLock`) to keep the thread safe. 
- `_loaded`: An event () `threading.Event`that controls the loading state of the object. 

**Code Description**:
The ThreadSafeObject class provides a thread-safe way to access and modify objects by encapsulating objects, keys, the cache pool they belong to, and synchronization mechanisms (re-entrant locks and events). With `acquire` the method  , you can safely get a reference to an object, perform an operation, and automatically release the lock when the operation is complete. In addition, the`start_loading` and `finish_loading` method allows you to control the loading state of an object, while `wait_for_loading` the method  can block the current thread until the object is loaded. 

In the project, the ThreadSafeObject class is closely related to the CachePool class, which is responsible for managing the ThreadSafeObject instances in the cache. For example, the CachePool `get` method calls the method before returning the cached object `wait_for_loading` to ensure that the object has been loaded. `set` The and `pop` methods are used to add or remove instances of ThreadSafeObject from the cache. In addition,`acquire` methods provide a mechanism that allows a reference to an object to be securely obtained before performing an operation. 

The ThreadSafeObject class is also used as a base class for other specific types of objects, such as the ThreadSafeFaiss class, which adds FAISS-related features such as document counting and saving to disk on top of ThreadSafeObject.

**Note**:
- When working with shared resources in a multithreaded environment, using ThreadSafeObject avoids data races and other concurrency issues.
- When using `acquire` methods, you should make sure to use `with` statements or manually release locks to avoid deadlocks. 
- When modifying `_obj` a property, you should go through `obj` the property's setter method to ensure thread-safety. 

**Example output**:
Suppose you have an instance of ThreadSafeObject `_key` that is a "example_key",`_obj` which is a custom object. Calling `__repr__` the method might return a string like this:
`"<ThreadSafeObject: key: example_key, obj: <自定义对象的表示>>"`
### FunctionDef __init__(self, key, obj, pool)
**__init__**: This function is used to initialize the ThreadSafeObject object. 

**Parameters**:
- `key`: can be a string or tuple and is used to identify an object.
- `obj`: An object assigned to a ThreadSafeObject at initialization, which defaults to None.
- `pool`: A CachePool instance that stores cache objects, which is None by default.

**Code Description**:
This `__init__`method `ThreadSafeObject`is the constructor of the class, which is responsible for initializing a thread-safe object. It receives three parameters:`key` , `obj`, and`pool` . `key`is an identifier, which can be a string or tuple, that uniquely identifies the object. `obj`The parameter is of any type and represents a data object that needs to be accessed by threads safely, and the default value is None. `pool`A parameter is an `CachePool`instance of a type, which is an optional parameter with a default value of None, which specifies the cache pool to which the object belongs. 

In the initialization process of the object, the input`obj``key` `pool`and and parameters are first assigned to the internal variables`_obj`, `_key`and`_pool` respectively. Next,`threading.RLock()` create a Reentrant Lock and assign it to `_lock`a property, which ensures thread-safe access to the object. Finally, an`threading.Event()` instance is created to assign a property to the `_loaded`event object that controls the synchronization of the object's loading state. 

**Note**:
- When operating the same instance in a multi-threaded environment`ThreadSafeObject`, ensure proper use `_lock`to avoid data contention. 
- `key`The parameter is required because it is used to uniquely identify an`ThreadSafeObject` instance. 
- If parameters are provided`pool`, then this `ThreadSafeObject`instance will be associated with the specified cache pool, which is useful when managing multiple cache objects. 
***
### FunctionDef __repr__(self)
**__repr__**: The function of this function is to return an official string representation of the object. 

****Arguments: This function has no arguments. 

**Code Description**: `__repr__` A method is a special method that defines the "official" string representation of an object. In this implementation,  the `type(self).__name__` class name of the object is first obtained by , and then a formatted string is constructed and returned in combination with the object's `key` properties and `_obj` attributes. This string is `<类名: key: 键值, obj: 对象值>` presented in the format of , where `键值` is obtained  by calling the object `key` 's method, and  directly `对象值` accessing the object's `_obj` properties. This representation provides not only basic information about the object, but also key data about the object, making debugging and logging easier. 

From the perspective of the structure of the project,`__repr__` methods `key` have a direct invocation relationship with methods. `key` Methods are used to get the key value of an object, which is a unique identifier for an object in a cache or other data structure. In a `__repr__` method, `key` you can get this key value by calling the method and include it in the string representation of the object. Doing so can help you quickly identify objects when logging or debugging. 

**Note**: When using `__repr__` methods, you need to make sure that the object's `_key` and `_obj` properties have been initialized correctly, otherwise it may cause an error. Also, considering that `__repr__` the output of the method may be used for logging, you should ensure that the information contained is useful and not too verbose. 

**Example output**: Suppose the class name of the object is , `ThreadSafeObject`the`_key` value of the property is `"example_key"` , and`_obj` the value of the property is `"example_object"` , then calling `__repr__` the method  will return:
```
<ThreadSafeObject: key: example_key, obj: example_object>
```
***
### FunctionDef key(self)
**key**: The function of this function is to get the key value of the object. 

****Arguments: This function has no arguments. 

**Code Description**: `key` A function is a simple but critical part of accessing and returning the properties of an object `_key` . This property usually represents a unique identifier of an object in a cache or other data structure. In a multi-threaded environment, accessing and managing these key-values is an important mechanism to ensure data consistency and thread safety. 

In the case of calls in the project,`key` functions are called in several places, showing their importance in object representation (`__repr__`methods), resource fetches (`acquire`methods), and specific operations such as saving and emptying the cache (`save`and `clear` methods). For example, in a `__repr__` method,  you `key` can call a function to get the key value of an object to build and return a string representation of the object, which helps with debugging and logging. In the `acquire` method,`key` the return value of the function is used for logging, helping to track which thread is working on which resource. In the `save` and `clear` methods,`key` it is also used for logging, providing contextual information about the operation. 

**Note**: When using this function, you need to make sure that the  property `_key` has been initialized correctly, otherwise an error may be thrown. In addition, due to thread safety, `_key` synchronization issues should be handled with caution when accessing properties, and although this function may seem simple in its implementation, it should be used with caution when used in a multi-threaded environment. 

**Example output**: Assuming `_key` that the value of the property is `"example_key"` , then calling `key` the function  will return:
```
"example_key"
```
***
### FunctionDef acquire(self, owner, msg)
**acquire**: The function of this function is to securely fetch and manipulate object resources. 

**Parameters**:
- `owner`: String type, which is an empty string by default, indicates the owner of the resource. If not provided, the ID of the current thread is used by default.
- `msg`: String type, which is an empty string by default, and is used to append additional log information.

**Code Description**:
`acquire` A function is a context manager that securely acquires and releases resources in a multithreaded environment. It first tries to acquire a lock to ensure thread-safety when manipulating an object's resource. If a parameter is provided`owner`, the value of the parameter is used as the owner of the resource. If it is not provided, the ID of the current thread is used as the owner by default. In addition, if a property is present`_pool` and is not`None`, a method is called `_pool._cache.move_to_end(self.key)`to move the key value of the current object to the end of the cache, which is typically used to maintain the cache's LRU (Least Recently Used) policy. 

Before and after the lock is successfully acquired and the resource operation is performed, if `log_verbose`true, log information is recorded, including the start and end of the operation, as well as the information provided`msg`. This helps you track resource usage and debugging. 

In a `finally`block, regardless of whether the resource operation is successful or not, the previously acquired locks will be released to ensure the safe release of resources and avoid deadlocks. 

**Note**:
- When using `acquire`functions, you need to make sure that the `_lock`property has been properly initialized as a lock object, otherwise an exception will be thrown when trying to acquire a lock. 
- When working with shared resources in a multi-threaded environment, it is important to use locks correctly to avoid data contention and inconsistencies.
- `acquire`The function is designed as a context manager, and it is recommended `with`to use statements to make calls to ensure that resources are properly acquired and released. 
***
### FunctionDef start_loading(self)
**start_loading**: The function of this function is to clear the loading state. 

****Arguments: This function has no arguments. 

**Code description**: `start_loading` A function is `ThreadSafeObject` a method of the class that resets the loading state of an object. In this method, `self._loaded.clear()` this is done by calling . `_loaded` is a flag that indicates whether an object's data has been loaded. Calling  the method `clear` resets this flag, meaning that the object's loaded state is cleared and the object is considered unloaded. This is usually done to prepare the object when the data needs to be reloaded, ensuring that the latest state of the data can be reloaded and used. 

**Note**: When using `start_loading` methods, you need to ensure that any operation that depends on the loading state of an object handles the unloaded state of an object correctly. Also, considering that this is a thread-safe object,`start_loading` method calls should be made with an appropriate synchronization mechanism to avoid problems caused by concurrent access. 
***
### FunctionDef finish_loading(self)
**finish_loading**: The function of this function is to mark the completion of the object load. 

****Arguments: This function has no arguments. 

**Code Description**: `finish_loading` A function is a method of a class that notifies other threads that may be waiting for the object to be loaded `ThreadSafeObject`after the loading or initialization process of an object is completed by setting an internal thread-safe flag (e.g`threading.Event``set`., a method used). In this project, `finish_loading`methods are called in a number of places, mainly to mark the state of the Embeddings or Vector Store. 

In the`load_embeddings` method, `finish_loading`it is called to mark the completion of an embedded model object load. This process involves selecting the appropriate embedded model, loading the model, assigning model objects to`ThreadSafeObject` the instance's `obj`properties, and finally `finish_loading`marking the loading process by calling methods. 

In `load_vector_store`methods, both in`KBFaissPool` and `MemoFaissPool`in classes, `finish_loading`it is also used to mark the completion of the vector storage load. The process of loading a vector store may involve loading an existing vector store from disk, or creating a new empty vector store, and then assigning this vector store object to`ThreadSafeFaiss` the properties of the instance`obj` and marking the load as`finish_loading` complete by a method. 

**Note**: When using `finish_loading`a method, you need to make sure that this method is called after the loading or initialization logic of the object is completed correctly. In addition, this method is usually preceded by a thread lock operation to ensure thread safety. After the call`finish_loading`, other threads can follow up by checking the corresponding thread-safe flag to determine if the object has been loaded. 
***
### FunctionDef wait_for_loading(self)
**wait_for_loading**: The function of this function is to wait until the object is loaded. 

****Arguments: This function has no arguments. 

**Code Description**:  A `wait_for_loading` function is `ThreadSafeObject` a method of the class that is used to ensure that objects are loaded safely in a multithreaded environment. This is done by calling `_loaded` a  method of a property (a thread-safe event object). `wait` When `_loaded` an event is set, it means that the object has finished loading, and `wait` the method  stops blocking and allows subsequent code to be executed. If  the `_loaded` event has not already been set, the thread that calls this method will be blocked until the event is set. This mechanism ensures that any operations that depend on the state of the object are paused until the object is fully loaded, avoiding potential data inconsistencies or race condition issues. 

**Note**: `wait_for_loading` When using a method, you need to make sure that  the `_loaded` event is set correctly after the object is loaded, otherwise the thread calling this method may block indefinitely. In addition, given the complexity of multi-threaded programming, developers should carefully manage synchronization and communication between threads to avoid issues such as deadlocks or resource contention. 
***
### FunctionDef obj(self)
**obj**: The function of this function is to get the _obj properties in the ThreadSafeObject object. 

****Arguments: This function has no arguments. 

**Code Description**: `obj`A function is a simple accessor that returns properties from a ThreadSafeObject instance`_obj`. In a multi-threaded environment, the ThreadSafeObject object provides a thread-safe access method to ensure that the state of the object is consistent during concurrent access. In a project,`obj` functions are used in a number of scenarios, mainly to get instances of objects that have been loaded or created when loading embeddings and vector stores. 

For example, in the `load_embeddings`method, first check if the embedding vector for the specified model and device has been loaded, and if not, create a new instance of ThreadSafeObject and`obj` set the embedding vector object via the function. In the `load_vector_store`method, the same logic is applied to load or create a vector store instance. This usage ensures that access to embedding vectors and vector stores is thread-safe in a concurrent environment. 

**Note**: When using `obj`functions, you need to make sure that the properties of the ThreadSafeObject instance `_obj`have been initialized correctly. Otherwise, the object will be returned or in`None` its initial state, which may result in an error in subsequent operations. 

**Output example**: Suppose the property of the ThreadSafeObject instance `_obj`is set to an embedding vector object, then the calling `obj`function will return the embedding vector object. For example:

```python
embeddings = thread_safe_object_instance.obj()
```

Here, `embeddings`it will be the embedding vector object that was previously stored in the ThreadSafeObject instance. 
***
### FunctionDef obj(self, val)
**obj**: The obj function is used to set the internal object of the ThreadSafeObject instance. 

**Parameters**:
- `val`: Any type, indicating the value to be set.

**Code Description**:
The obj function is a member method of the ThreadSafeObject class, whose main function is to assign incoming parameters`val` to the properties of the instance`_obj`. This approach is fundamental to thread-safe object operations and allows for safe changes to the state of objects in a multi-threaded environment. 

In the project, obj functions are used in different contexts, mainly related to loading and setting up embedded objects or vector storage. For example`EmbeddingsPool``load_embeddings`, in the method, the obj function is used to assign a value to a loaded embedded model object to a ThreadSafeObject instance. Doing so ensures that the loading and access of embedded model objects is thread-safe when accessing concurrently. 

Similarly, in the`KBFaissPool` AND`MemoFaissPool` `load_vector_store`method, the obj function is used to set the vector storage object to be loaded or created. These methods first check if the desired vector store already exists in the cache, and if it doesn't, create a new instance of ThreadSafeFaiss and assign the vector store object to it via the obj function. This ensures that the loading and initialization process for vector stores is thread-safe. 

**Note**:
- When using an obj function, you need to make sure that the arguments you pass in`val` are of the correct type, as there is no type checking inside the function. 
- When using obj functions to modify the state of objects in a multi-threaded environment, attention should be paid to synchronization and concurrency control to avoid data contention and inconsistency. Although the operation of the obj function itself is a simple assignment, its use cases in projects often involve thread-safe contexts, so the correct way to use it is essential to maintain the stability and correctness of the program.
***
## ClassDef CachePool
**CachePool**: The function of the CachePool class is to provide a thread-safe cache pool for storing and managing cached objects. 

**Properties**:
- `_cache_num`: The maximum number of cached objects allowed to be stored in the cache pool. If set to -1, there is no limit to the quantity.
- `_cache`: An ordered dictionary that stores cached objects.
- `atomic`: A thread lock that ensures thread safety for cache operations.

**Code Description**:
The CachePool class provides a thread-safe implementation of cache pools that allow users to store, acquire, and manage cached objects. It uses an ordered dictionary `_cache` to store cached objects, where the key is the identifier of the cached object and the value is the cached object itself. `atomic` Thread locks ensure thread safety for caching operations. 

- `__init__` Method initializes the cache pool, which allows you to specify the maximum number of cached objects allowed in the cache pool.
- `keys` The method returns a list of all keys in the current cache.
- `_check_count` method checks the number of caches at hand, and if the set maximum is exceeded, removes the oldest cached object.
- `get` The method gets the cached object based on the key. If the object exists, wait for the object to be loaded and returned.
- `set` The method adds an object to the cache and removes the oldest cached objects as needed to stay within the maximum number limit.
- `pop` The method removes and returns cached objects for the specified key. If no key is specified, the oldest cached object is removed and returned.
- `acquire` The method attempts to obtain the cache object of the specified key and lock it to ensure data consistency in a concurrent environment.
- `load_kb_embeddings` The method is used to load the knowledge base embedding vector, which loads the embedding vector based on the knowledge base name, embedding device, and default embedding model.

The CachePool class is called by other objects in the project, such as `EmbeddingsPool`  and , `_FaissPool` and is used to manage the embedding vector and the cache of the vector store. These invocations show that the CachePool class plays a central role in knowledge base embedding vector and vector storage management, providing caching management and thread-safe support for the upper layer. 

**Note**:
- When operating caching in a multi-threaded environment, you should ensure that `atomic` locks are used correctly  to avoid data contention. 
- When setting  a `_cache_num` limit on the number of caches, be aware that the cache retirement policy may affect the availability of cached objects. 

**Example output**:
Because the CachePool primarily provides cache management capabilities, its output depends on the type of object stored in the cache. For example, if the cache is stored with an embedding vector object, the `get` method  might return an instance of the embedding vector object. 
### FunctionDef __init__(self, cache_num)
**__init__**: The function of this function is to initialize the CachePool object. 

**Parameters**:
- `cache_num`: Integer, which indicates the maximum number of elements allowed in the cache, and the default value is -1, which indicates that the number is unlimited.
- `self._cache`: Uses `OrderedDict`initialization, which is used to store cached data, maintaining the insertion order. 
- `self.atomic`: Use `threading.RLock`initialization to provide a thread-based lock that controls concurrent access to cached data and ensures thread-security. 

**Code Description**:
This function is the `CachePool`constructor of the class that is used to initialize a cache pool object. It accepts a parameter`cache_num` that specifies the maximum number of elements that can be stored in the cache. If`cache_num` the value is -1, the cache size is unlimited. Internally, `cache_num`the function first assigns the value of the parameter to the object's`_cache_num` properties, which is used to control the cache size later. Next, use`OrderedDict` the initialization`_cache` attribute, `OrderedDict`which is a special dictionary that remembers the order in which elements were inserted, which is useful for some cache elimination strategies, such as the recent use of LRUs. Finally, by`threading.RLock` creating a reentrant lock`atomic`, the properties assigned to the object are assigned`atomic`. This lock is used to synchronize access to the cache, ensuring that operations on the cache are thread-safe in a multi-threaded environment. 

**Note**:
- When operating caching in a multi-threaded environment, you should ensure that locks are used correctly`self.atomic` to avoid data contention and inconsistencies. 
- `cache_num`The default value is -1, which means that the cache size is not limited unless otherwise specified. In practice, this parameter should be set reasonably as needed to avoid consuming too much memory resources due to excessive cache.
- `OrderedDict`While it is possible to maintain the order in which elements are inserted, it can have a higher performance overhead than a normal dictionary when processing large amounts of data, so this should be taken into account when designing a caching strategy.
***
### FunctionDef keys(self)
**keys**: What this function does is get a list of all the keys in the cache. 

****Arguments: This function has no arguments. 

**Code Description**: `keys` A function is `CachePool` a method of a class whose main purpose is to retrieve all keys from the cache and return those keys as a list of strings. In this function,`self._cache.keys()` the  call takes `_cache` all the keys in the dictionary and `list()` converts them into a list via the function. This is a very basic but important feature because it allows the other parts of the code to know what data is currently stored in the cache. 

In the project, this function is `file_chat` called by a function to check if the incoming `knowledge_id` is  present in the `memo_faiss_pool` cache. If  is `knowledge_id` not in the cached key, the`file_chat` function will return an error response stating that the required temporary knowledge base was not found. This indicates that `keys` functions are used in the project for validation and retrieval operations, ensuring that the required data has been properly stored in the cache before further processing. 

**Note**: When using this function, you need to make sure that  it `_cache` has been initialized correctly and contains the required data. In addition, the returned key list only represents the state in the cache at the time the function was called, and subsequent updates to the cached content will not be reflected in the returned list. 

**Example output**: Suppose there are three keys stored in the cache, which are `"key1"`, `"key2"`, `"key3"`then calling  the function `keys` will return the following list:
```python
["key1", "key2", "key3"]
```
***
### FunctionDef _check_count(self)
**_check_count**: The function of this function is to check the number of items in the cache and make sure that it does not exceed the set maximum. 

****Arguments: This function has no arguments. 

**Code Description**:  A `_check_count` function is `CachePool` a private method of the class that maintains that the number of items in the cache pool does not exceed a preset maximum. This function first checks if the member variable `_cache_num` is an integer and greater than 0. If so, the function enters a loop if the length of the cache pool `_cache` is greater than  .`_cache_num` Inside the loop, use  the `_cache.popitem(last=False)` Remove the oldest added item from the cache until the size of the cache does not exceed  .`_cache_num` This mechanism ensures that the cache pool does not grow indefinitely, thus effectively managing memory usage. 

In the project, it`_check_count` is called by `set` a method. `set` Method for adding a new item to the cache and calling as soon as it is added `_check_count` ensures that the size of the cache pool does not exceed the preset limit. This shows that `_check_count` it plays a key role in the cache management strategy, which ensures the robustness and stability of the caching system by limiting the cache size to prevent memory overflow. 

**Note**: `_check_count` This is a private method, meaning that it is only `CachePool` used inside the class and should not be called directly outside the class. This design encapsulates the details of cache management, making `CachePool` the use of classes more secure and convenient. When using `CachePool` classes, developers don't need to manage the cache size directly, but indirectly by setting `_cache_num` and  using `set` methods. 
***
### FunctionDef get(self, key)
**get**: The function of this function is to get the thread-safe object associated with a given key from the cache pool. 

**Parameters**:
- `key`: A string type that is used to retrieve the key of an object from the cache.

**Code Description**:
`get` The function first tries to  get an object `_cache` from the cache pool using the given key `key` . If an object is found, the function calls the object's `wait_for_loading` method. What this does is block the current thread until the object's loading state is set to complete. This ensures that the object is already available before it is returned. If no corresponding key is found in the cache, the function will not return any value. 

In a project,`get` functions are called in a number of places, including, but not limited to, loading embedding vectors, saving and unloading vector stores, and manipulating vector stores in worker threads. These call scenarios show that functions`get` are a critical component in handling cached objects, especially if you need to make sure that the object is loaded before proceeding. 

**Note**:
- When using `get` functions, you should ensure that the provided key `key` actually exists in the cache, otherwise the function will return `None`. 
- In a multi-threaded environment,`get` the function `wait_for_loading` ensures thread-safety through the method and avoids race conditions before the object is loaded. 

**Example output**:
Let's say there is an `"example_key"` instance of key in  the  cache `ThreadSafeObject` and the instance has finished loading. Calling `get("example_key")` will  return that `ThreadSafeObject` instance. If  is `"example_key"` not present in the cache, the function will return `None`. 
***
### FunctionDef set(self, key, obj)
**set**: The function of this function is to add a thread-safe object to the cache pool and return that object. 

**Parameters**:
- `key`: A string type that identifies the object in the cache.
- `obj`: `ThreadSafeObject` Type, which represents the thread-safe object to be added to the cache. 

**Code Description**: `set` The function first stores the incoming thread-safe object `obj` and its corresponding key `key` in the cache pool's internal dictionary `_cache` . This ensures that objects can be quickly retrieved by key-values. The function then calls `_check_count` the method to check if the number of objects in the cache pool exceeds the preset maximum, and if so, the oldest objects are automatically removed to keep the size of the cache pool within the limit. Finally, the function returns the thread-safe object you just added `obj`. 

In the project,`set` functions are used in several scenarios, including but not limited to loading embedding vectors (`load_embeddings`), loading vector stores (`load_vector_store`), etc. In these scenarios,`set` the function is responsible for adding newly created or loaded resources (such as embedding vectors, vector stores) to the cache pool in a thread-safe manner to ensure that these resources can be accessed efficiently and securely in the future. 

**Note**:
- When using `set` functions, you need to make sure that the keys you pass in `key` are unique in the cache pool to avoid overwriting existing cached items. 
- Since `set` the function checks the size of the cache pool and removes the oldest cache items if necessary, the developer should set the maximum size of the cache pool to `_cache_num`balance memory usage and performance requirements. 
- In a multi-threaded environment,`set` functions ensure thread-safe access and operations when adding cached items, but you still need to pay attention to thread-safe access and operations when using cached items. 

**Example of output**: Suppose the calling `set` function adds a  cached item with a key to and an `"example_key"`object to an `ThreadSafeObject` instance, the function will return that `ThreadSafeObject` instance. 
***
### FunctionDef pop(self, key)
**pop**: This function is used to remove from the cache pool and return the object with the specified key or the earliest object to be added. 

**Parameters**:
- `key`: String type, specifying the key from which you want to remove the object. The default value is None, which removes and returns the oldest added object.

**Code Description**:
`pop` A function is `CachePool` a method of the class that is used to remove the corresponding object from the cache and return the corresponding object based on a given key. If no key is provided when called (i.e`key=None`., ), the function removes and returns the oldest object added to the cache. This is achieved by calling `_cache` the dictionary's `popitem` method, where  the `last=False` parameter ensures that the oldest added item is returned. If a key is provided, `_cache` `pop` the object associated with that key is attempted to be removed and returned via the dictionary method. If the key does not exist, it is returned`None`. 

In a project,`pop` methods are called by multiple scenarios, such as in `upload_temp_docs` functions, to remove previous temporary documents; In the `unload_vector_store` method, it is used to release the vector library; In `do_clear_vs` the method, it is used to clear a specific vector store; and in the `drop_kb_summary` method, for deleting the knowledge base summary. These invocation scenarios show that `pop` methods play a key role in managing cache resources, maintaining cache state, and freeing up resources that are no longer needed. 

**Note**:
- When using `pop` methods, you should ensure that the keys are correct and existent, especially if you want to remove a particular object. If the key doesn't exist, the method will return `None`instead of throwing an exception. 
- When you don't need to specify a key to remove an object, you should note that  the method `pop` will remove and return the oldest added object, which may affect the logic of using the cache. 

**Example output**:
Suppose there is an object in the cache with the key of "example_key", `ThreadSafeObject` and calling  will `pop("example_key")` return the object and remove it from the cache. If the cache is empty or the key doesn't exist, the call `pop("nonexistent_key")` will return`None`. 
***
### FunctionDef acquire(self, key, owner, msg)
**acquire**: The function of this function securely fetches the object associated with a given key from the cache pool. 

**Parameters**:
- `key`: A string or tuple type that is used to retrieve the key of an object from the cache.
- `owner`: String type, which defaults to an empty string and represents the owner of the request object.
- `msg`: A string type, which defaults to an empty string and is used to append a message or description.

**Code Description**:
`acquire` The function first `get` tries to get the object associated with a given key from the cache pool by calling the method `key` . If the object corresponding to the key does not exist in the cache, the function will throw an `RuntimeError` exception to indicate that the requested resource does not exist. If an object is successfully fetched, and the object is an `ThreadSafeObject` instance of type , the object's  method is called `acquire` to safely get a reference to the object and return it. This process involves thread-safe processing to ensure that access to objects is secure in a multi-threaded environment. If the obtained object is not `ThreadSafeObject` an instance of type , the object is returned directly. 

In a project,`acquire` functions are used to securely fetch objects in the cache for subsequent operations. For example, in a `knowledge_base_chat_iterator` function, you can call  a `acquire` method to get a vector store object in your knowledge base to perform operations such as a similarity search. 

**Note**:
- When using `acquire` functions, you should make sure that the provided key `key` actually exists in the cache, otherwise an exception will be thrown. 
- When the acquired object is an `ThreadSafeObject` instance of type , you should  use a statement `with` or other means to ensure that the lock is released after the operation is complete to avoid potential deadlock issues. 
- `acquire` The use cases of the method are mainly focused on situations where thread-safe access and manipulation of cached objects are required.

**Example output**:
Because `acquire` the return value of a function depends on the type of object in the cache, it may have different forms of return. If an object in the cache is an `ThreadSafeObject` instance of type , the return value will be a reference to that object; If it's a different type of object, the object is returned directly. For example, if there is an instance with the key of `"example_key"` in  the `ThreadSafeObject` cache  , calling  will `acquire("example_key")` return a reference to that instance. If `"example_key"` it corresponds to an object of type other `ThreadSafeObject` than that, the object is returned directly. 
***
### FunctionDef load_kb_embeddings(self, kb_name, embed_device, default_embed_model)
**load_kb_embeddings**: The function of this function is to load the embedding vector with the specified knowledge base name. 

**Parameters**:
- `kb_name`: String type, specifying the name of the knowledge base where you want to load the embedding vector.
- `embed_device`: String type, the default value is determined by `embedding_device`the function, and is used to specify the computing device. 
- `default_embed_model`: String type, default is used `EMBEDDING_MODEL`to specify the default embedding model. 

**Code Description**:
This function first `knowledge_base_repository`calls the function from in`get_kb_detail`, based on the details of the `kb_name`knowledge base, including the embedding model name. If the knowledge base details contain the embedded model name, that name is used; Otherwise, use the passed as the`default_embed_model` embedding model name. The function then checks whether the embedding model is in the online model list, which is provided by the`list_online_embed_models` function. If the embedding model exists in the online model list, `EmbeddingsFunAdapter`an embedding vector adapter instance is created via the class and returned. If the embedding model is not in the list of online models, the method that is called`embeddings_pool` loads `load_embeddings`the embedding vector based on the model name and device type, and returns the loaded embedding vector instance. 

**Note**:
- When you call this function, you need to make sure that you are passing in `kb_name`the name of the existing knowledge base and that there is corresponding embedding model information in the knowledge base. 
- `embed_device`Parameters should be based on the actual computing environment, such as`"cuda"` , `"mps"`or`"cpu"`. 
- This function depends on`EmbeddingsFunAdapter` the sum`embeddings_pool` of classes `load_embeddings`and methods, so you should make sure that the dependencies are configured correctly before using them. 

**Example output**:
Assuming that the name of the knowledge base is Technical Documentation Library, and the embedded model used by the knowledge base is in the list of online models, an instance may be returned`EmbeddingsFunAdapter`. If the embedding model is not in the list of online models, an `load_embeddings`instance of the embedding vector loaded by the method may be returned, depending on the embedding model loaded. 
***
## ClassDef EmbeddingsPool
**EmbeddingsPool**: The function of the EmbeddingsPool class is to manage and load embedding vectors for different models. 

**Properties**:
- There are no specific exposed properties, inherited from the properties of the CachePool class.

**Code Description**:
The EmbeddingsPool class inherits from the CachePool class and is specifically designed to load and manage embedding vectors. It provides a `load_embeddings` method that is responsible for loading embedding vectors based on the specified model and device. The method first tries to get the embedding vector from the cache, and if it doesn't exist in the cache, it creates the corresponding embedding vector object according to the model type and adds it to the cache. 

When loading embedding vectors, the EmbeddingsPool class calls different embedding vector classes depending on the model. For example, for OpenAI's "text-embedding-ada-002" model, it uses `OpenAIEmbeddings` classes; For models that contain "bge-", it selects the class according to the model language `HuggingFaceBgeEmbeddings` and sets the corresponding query instructions; For other models, it defaults to using `HuggingFaceEmbeddings` classes. 

In addition,`load_embeddings` the method will lock the embedding vector to `atomic` ensure thread safety before loading it, so as to avoid data contention in concurrent environments. Once loaded, the embedding vector object is stored in the cache for quick fetching. 

**Note**:
- When using `load_embeddings` methods, you need to make sure that the model and device parameters passed in are correct, otherwise you may not be able to load the correct embedding vectors. 
- When this class is used in a multi-threaded environment, its internal thread-safe mechanisms protect the loading process of embedding vectors, but there are other aspects of thread-safety that callers need to be aware of.
- Because embedding vectors can take up a lot of memory, you should manage the cache size appropriately to avoid memory overflow.

**Example output**:
 `load_embeddings` An example of an embedding vector object that might be returned by calling the method:
```python
embeddings = embeddings_pool.load_embeddings(model="text-embedding-ada-002", device="cuda")
```
This line of code returns an object for the "text-embedding-ada-002" model `OpenAIEmbeddings` , which is configured with all the parameters needed to interact with the OpenAI API and ready to compute the embedding vector on the specified device. 
### FunctionDef load_embeddings(self, model, device)
**load_embeddings**: The function of this function is to load and return embedding vector objects on the specified model and device. 

**Parameters**:
- `model`: String type, specifying the name of the embedding model to be loaded. If not provided, the default embedding model is used.
- `device`: String type, specifying the computing device. If it is not provided, the `embedding_device`appropriate device is automatically detected and selected through the function. 

**Code Description**:
The function first attempts to acquire a thread-safe lock to ensure operational safety in a multithreaded environment. Then, based on the model name and device type provided, a key-value pair is constructed`key` to retrieve or store the embedding vector object. If the corresponding embedding vector object does not exist in the cache, the function will create a new`ThreadSafeObject` instance and load the corresponding embedding vector according to the model name. 

If the model name is`"text-embedding-ada-002"`, load the embedding model provided by OpenAI. If the model name contains`"bge-"`, load the HuggingFace Bge embedding model of the corresponding language based on the language identifier in the model name (such as`"zh"` or or`"en"`), and set the corresponding query commands. For other model names, the embedding model provided by HuggingFace will be loaded. 

Once the load is complete, the embedded vector object is assigned to`ThreadSafeObject` the instance's `obj`properties and marked as loaded. If the corresponding embedding vector object already exists in the cache, the object is returned directly. 

**Note**:
- When using this function, you should ensure that the model name and compute device type provided are correct so that the embedding vector is loaded correctly.
- Multi-threaded security mechanisms, including lock sums, are used inside the function`ThreadSafeObject` to ensure operational safety in concurrent environments. 
- It can take some time to load embedding vectors, especially when they are first loaded, so you should design your application logic with possible latency in mind.

**Example output**:
The call `load_embeddings(model="text-embedding-ada-002", device="cuda")`may return an `OpenAIEmbeddings`instance that has been loaded with the specified OpenAI embedding model and is ready to perform the embedding vector computation on the CUDA device. 

In the project, `load_embeddings`functions are called by`load_kb_embeddings` and `load_local_embeddings`other functions to load knowledge base embedding vectors or local embedding vectors to support different application scenarios, such as text similarity calculation, text retrieval, etc. 
***
