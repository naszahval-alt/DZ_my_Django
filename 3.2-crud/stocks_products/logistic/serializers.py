from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'products']

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position_data in positions_data:
            StockProduct.objects.update_for_create(
                stokc=stock,
                product=position_data['product'],
                defaults={
                    'quantity': position_data['quantity'],
                    'price': position_data['price']
                }
            )

        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        existing_positions = set(stock.positions.values_list('product_id', flat=True))
        new_positions = {pos_data['product'].id for pos_data in positions_data}
        to_delete = existing_positions - new_positions

        stock.positions.filter(product_id_in=to_delete).delete()

        for position_data in positions_data:
            StockProduct.object.update_or_create(
                stock=stock,
                product=position_data['product'],
                defaults={
                    'quantity': position_data['quantity'],
                    'price': position_data['price']
                }
            )

        return stock
