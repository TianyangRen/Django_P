from django.db import models

# Promotion=========================================================================================================
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

# Collection=========================================================================================================
class Collection(models.Model):
    title = models.CharField(max_length=255)

    # 关系：Collection 多对一 Product（多个 Collection 可以主推同一个 Product）
    # 正向：collection.featured_product        → 返回一个 Product 对象  （这个分类主推哪个商品）
    # 反向：product.collection_set.all()       → 返回多个 Collection 对象（哪些分类主推了这个商品）
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

# Product=========================================================================================================
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    # 关系：Product 多对一 Collection（多个 Product 属于同一个 Collection）
    # 正向：product.collection                 → 返回一个 Collection 对象（这个商品属于哪个分类）
    # 反向：collection.product_set.all()       → 返回多个 Product 对象  （这个分类下有哪些商品）
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)

    # 关系：Product 多对多 Promotion（一个商品可以有多个促销，一个促销可以用于多个商品）
    # 正向：product.promotions.all()           → 返回多个 Promotion 对象（这个商品有哪些促销活动）
    # 反向：promotion.product_set.all()        → 返回多个 Product 对象  （这个促销活动用于哪些商品）
    promotions = models.ManyToManyField(Promotion)

# Customer=========================================================================================================
class Customer(models.Model):

    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
        ]

# Order=========================================================================================================
class Order(models.Model):

    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)

    # 关系：Order 多对一 Customer（一个 Customer 可以有多个 Order）
    # 正向：order.customer                     → 返回一个 Customer 对象（这个订单属于哪个用户）
    # 反向：customer.order_set.all()           → 返回多个 Order 对象   （这个用户的所有历史订单）
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

# OrderItem=========================================================================================================
class OrderItem(models.Model):

    # 关系：OrderItem 多对一 Order（一个 Order 包含多个 OrderItem）
    # 正向：orderitem.order                    → 返回一个 Order 对象     （这条记录属于哪个订单）
    # 反向：order.orderitem_set.all()          → 返回多个 OrderItem 对象 （这个订单里有哪些商品行）
    order = models.ForeignKey(Order, on_delete=models.PROTECT)

    # 关系：OrderItem 多对一 Product（同一个 Product 可以出现在多个 OrderItem）
    # 正向：orderitem.product                  → 返回一个 Product 对象   （这条记录是哪个商品）
    # 反向：product.orderitem_set.all()        → 返回多个 OrderItem 对象 （这个商品出现在哪些订单里）
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

# Address=========================================================================================================
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # 关系：Address 一对一 Customer（一个 Customer 只有一个 Address）
    # 正向：address.customer                   → 返回一个 Customer 对象（这个地址属于哪个用户）
    # 反向：customer.address                   → 返回一个 Address 对象 （这个用户的地址是什么）
    # ⚠️ 注意：一对一的反向查询没有 _set，直接用小写模型名 customer.address
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

# Cart=========================================================================================================
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

# CartItem=========================================================================================================
class CartItem(models.Model):

    # 关系：CartItem 多对一 Cart（一个 Cart 包含多个 CartItem）
    # 正向：cartitem.cart                      → 返回一个 Cart 对象      （这条记录属于哪个购物车）
    # 反向：cart.cartitem_set.all()            → 返回多个 CartItem 对象  （这个购物车里有哪些商品行）
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    # 关系：CartItem 多对一 Product（同一个 Product 可以出现在多个 CartItem）
    # 正向：cartitem.product                   → 返回一个 Product 对象   （这条记录是哪个商品）
    # 反向：product.cartitem_set.all()         → 返回多个 CartItem 对象  （这个商品出现在哪些购物车里）
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveSmallIntegerField()