---
source: "https://blog.hashhackers.com/blog/android-architecture-guide"
title: "Android Architecture: MVVM, Clean Architecture, and MVI"
fetched_at: "2026-10-06 12:33"
---

Apr 5, 2022 

# Android Architecture: MVVM, Clean Architecture, and MVI

* * *

Choosing the right architecture for an Android app separates maintainable projects from spaghetti codebases. Three patterns dominate modern Android development: MVVM, Clean Architecture, and MVI.

## MVVM with ViewModel

MVVM (Model-View-ViewModel) pairs naturally with Android’s lifecycle. The `ViewModel` survives configuration changes and exposes state via `StateFlow`.
    
    
    @HiltViewModel
    class ProductViewModel @Inject constructor(
        private val repository: ProductRepository
    ) : ViewModel() {
    
        private val _uiState = MutableStateFlow<ProductUiState>(ProductUiState.Loading)
        val uiState: StateFlow<ProductUiState> = _uiState.asStateFlow()
    
        init {
            loadProducts()
        }
    
        private fun loadProducts() {
            viewModelScope.launch {
                _uiState.value = ProductUiState.Loading
                repository.getProducts()
                    .onSuccess { products ->
                        _uiState.value = ProductUiState.Success(products)
                    }
                    .onFailure { error ->
                        _uiState.value = ProductUiState.Error(error.message ?: "Unknown error")
                    }
            }
        }
    }
    
    sealed class ProductUiState {
        object Loading : ProductUiState()
        data class Success(val products: List<Product>) : ProductUiState()
        data class Error(val message: String) : ProductUiState()
    }

## Clean Architecture Layers

Clean Architecture divides the codebase into three layers: **Presentation** , **Domain** , and **Data**.
    
    
    // Domain layer — use case
    class GetProductsUseCase @Inject constructor(
        private val productRepository: ProductRepository
    ) {
        suspend operator fun invoke(): Result<List<Product>> =
            productRepository.getProducts()
    }
    
    // Domain layer — repository interface
    interface ProductRepository {
        suspend fun getProducts(): Result<List<Product>>
        suspend fun getProductById(id: String): Result<Product>
    }
    
    // Data layer — repository implementation
    class ProductRepositoryImpl @Inject constructor(
        private val remoteDataSource: ProductRemoteDataSource,
        private val localDataSource: ProductLocalDataSource
    ) : ProductRepository {
    
        override suspend fun getProducts(): Result<List<Product>> {
            return try {
                val remote = remoteDataSource.fetchProducts()
                localDataSource.saveProducts(remote)
                Result.success(remote.map { it.toDomain() })
            } catch (e: Exception) {
                val cached = localDataSource.getProducts()
                if (cached.isNotEmpty()) Result.success(cached.map { it.toDomain() })
                else Result.failure(e)
            }
        }
    }

## MVI Pattern

MVI (Model-View-Intent) uses a unidirectional data flow with explicit intents and a single immutable state.
    
    
    // Intent — user actions
    sealed class ProductIntent {
        object LoadProducts : ProductIntent()
        data class SearchProducts(val query: String) : ProductIntent()
        data class SelectProduct(val id: String) : ProductIntent()
    }
    
    // State — single source of truth
    data class ProductState(
        val isLoading: Boolean = false,
        val products: List<Product> = emptyList(),
        val selectedProduct: Product? = null,
        val error: String? = null
    )
    
    @HiltViewModel
    class ProductMviViewModel @Inject constructor(
        private val getProducts: GetProductsUseCase
    ) : ViewModel() {
    
        private val _state = MutableStateFlow(ProductState())
        val state = _state.asStateFlow()
    
        fun processIntent(intent: ProductIntent) {
            when (intent) {
                is ProductIntent.LoadProducts -> loadProducts()
                is ProductIntent.SearchProducts -> searchProducts(intent.query)
                is ProductIntent.SelectProduct -> selectProduct(intent.id)
            }
        }
    
        private fun loadProducts() {
            viewModelScope.launch {
                _state.update { it.copy(isLoading = true, error = null) }
                getProducts()
                    .onSuccess { products -> _state.update { it.copy(isLoading = false, products = products) } }
                    .onFailure { e -> _state.update { it.copy(isLoading = false, error = e.message) } }
            }
        }
    }

## Collecting State in the Fragment
    
    
    @AndroidEntryPoint
    class ProductFragment : Fragment() {
    
        private val viewModel: ProductViewModel by viewModels()
    
        override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
            super.onViewCreated(view, savedInstanceState)
            viewLifecycleOwner.lifecycleScope.launch {
                repeatOnLifecycle(Lifecycle.State.STARTED) {
                    viewModel.uiState.collect { state ->
                        when (state) {
                            is ProductUiState.Loading -> showLoading()
                            is ProductUiState.Success -> showProducts(state.products)
                            is ProductUiState.Error -> showError(state.message)
                        }
                    }
                }
            }
        }
    }

## Choosing the Right Pattern

Pattern| Best For  
---|---  
MVVM| Most apps — simple, well-supported by Android  
Clean Architecture| Large teams, complex business logic  
MVI| Predictable state, time-travel debugging  
  
Start with MVVM and layer in Clean Architecture as your app grows. Add MVI when state complexity demands it.
