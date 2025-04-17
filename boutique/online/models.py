from django.db import models

# Create your models here.
class tbl_category_add(models.Model):
    name=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to='media',null=True)


class tbl_Product(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=100)  # Unique identifier for the product
    image=models.ImageField(upload_to="media",null=True)
    category=models.ForeignKey(tbl_category_add,on_delete=models.CASCADE,null=True,related_name="product")
    description=models.TextField(null=True)
    stock=models.IntegerField(null=True)
    original_price=models.FloatField(null=True)
    offer_price=models.FloatField(null=True)
    color=models.CharField(max_length=100,null=True)
    fabric=models.CharField(max_length=100,null=True)
    Pattern=models.CharField(max_length=100,null=True)
    WashCare=models.CharField(max_length=100,null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class tbl_ProductVariant(models.Model):
    product = models.ForeignKey(tbl_Product, related_name="variants", on_delete=models.CASCADE)
    color = models.CharField(max_length=50, blank=True, null=True)
    image=models.ImageField(upload_to="media",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class tbl_Register(models.Model):
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    mobile=models.IntegerField(null=True)
    password=models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class tbl_Cart(models.Model):
    product = models.ForeignKey(tbl_Product, related_name="carts", on_delete=models.CASCADE)
    user = models.ForeignKey(tbl_Register, related_name="register", on_delete=models.CASCADE, null=True)
    session_key = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(null=True)
    size = models.CharField(max_length=20, null=True)
    color = models.CharField(max_length=20, null=True)
    image=models.ImageField(upload_to="media",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def total_price(self):
        return self.quantity*self.product.offer_price

class Order(models.Model):
    user = models.ForeignKey(tbl_Register, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100,null=True)
    p_date=models.DateTimeField(null=True)
    d_date=models.DateTimeField(null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(tbl_Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20, null=True)
    color = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to="media", null=True)

class tbl_contact(models.Model):
    Name = models.CharField(max_length=50, blank=True, null=True)
    phone_no = models.IntegerField(null=True)
    email = models.EmailField(max_length=100, null=True)
    message =models.CharField(max_length=300, null=True )

class CustomDressOrder(models.Model):
    user=models.ForeignKey(tbl_Register,on_delete=models.CASCADE,null=True)
    dress_name = models.CharField(max_length=255)
    fabric = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    neck_design = models.CharField(max_length=100)
    custom_neck_design = models.CharField(max_length=255, blank=True, null=True)
    bust = models.FloatField()
    waist = models.FloatField()
    hips = models.FloatField()
    length = models.FloatField()
    delivery_date = models.DateField()
    reference_image = models.ImageField(upload_to='dress_references/', blank=True, null=True)
    additional_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100,null=True)
    total_cost=models.FloatField(null=True)
    advance=models.FloatField(null=True)
    payment_status=models.CharField(max_length=100,null=True)
    work_status=models.CharField(max_length=100,null=True)



