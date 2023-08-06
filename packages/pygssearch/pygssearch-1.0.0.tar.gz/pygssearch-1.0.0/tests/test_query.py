import unittest
import uuid

from pygssearch.query.query import query_builder


class TestQueryBuilder(unittest.TestCase):
    geo_path = 'tests/resources/geo.json'
    geo_query = "OData.CSC.Intersects(location=Footprint," \
                "area=geography'SRID=4326;Polygon(" \
                "(100.0 0.0,101.0 0.0,101.0 1.0,100.0 1.0,100.0 0.0))')"

    def test_default_query(self):
        query = query_builder()
        self.assertEqual(len(query), 2)
        self.assertIsNone(query[0], query[1])

    def test_filters_query(self):
        query = query_builder()
        self.assertEqual(len(query), 2)
        self.assertIsNone(query[0], query[1])

    def test_date_filter(self):
        query = query_builder(date=('2020-21-12', None))
        self.assertEqual(query[0].evaluate(), 'ContentDate/Start ge'
                                              ' 2020-21-12T00:00:00.0Z')

        query = query_builder(date=('2020-21-12T00:00:00.0Z', None))
        self.assertEqual(query[0].evaluate(), 'ContentDate/Start ge'
                                              ' 2020-21-12T00:00:00.0Z')

        query = query_builder(date=('NOW', None))
        self.assertEqual(query[0].evaluate(), 'ContentDate/Start ge NOW')

        query = query_builder(date=('2020-21-12', "2020-21-12"))
        self.assertEqual(
            query[0].evaluate(),
            'ContentDate/Start ge 2020-21-12T00:00:00.0Z and ContentDate/End '
            'lt 2020-21-12T00:00:00.0Z'
        )

        query = query_builder(date=(None, '2020-21-12'))
        self.assertIsNone(query[1])
        self.assertEqual(query[0].evaluate(), 'ContentDate/End'
                                              ' lt 2020-21-12T00:00:00.0Z')

    def test_geometry_filter(self):
        query = query_builder(geometry=self.geo_path)
        self.assertIsNone(query[1])
        self.assertEqual(query[0].evaluate(), self.geo_query)

        query = query_builder(geometry=('1,1', '0,1', '0,0'))
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "OData.CSC.Intersects(location=Footprint,"
            "area=geography'SRID=4326;Polygon((1.0 1.0,0.0 1.0,0.0 0.0))')"
        )

        query = query_builder(geometry=((1, 1), (0, 1), (0, 0)))
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "OData.CSC.Intersects(location=Footprint,"
            "area=geography'SRID=4326;Polygon((1.0 1.0,0.0 1.0,0.0 0.0))')"
        )

    def test_filter(self):
        query = query_builder(filters='my awsomeodatafilter', name=('s1abs',))
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "my awsomeodatafilter and contains(Name,'s1abs')"
        )

    def test_uuid_filter(self):
        query = query_builder(id=('123456',))
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "Id eq 123456"
        )

        query = query_builder(id='123456')
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "Id eq 123456"
        )

        query = query_builder(id=uuid.UUID(
            '3d641f34-af4e-4a08-b7b0-5c6bebc1cbfc'))
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "Id eq 3d641f34-af4e-4a08-b7b0-5c6bebc1cbfc"
        )

        query = query_builder(id=('123456', '7891011'))
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "(Id eq 123456 or Id eq 7891011)"
        )

    def test_name_filter(self):
        query = query_builder(name=('s1A_GRD',))
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "contains(Name,'s1A_GRD')"
        )

        query = query_builder(name='s1A_GRD')
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "contains(Name,'s1A_GRD')"
        )

        query = query_builder(name=('s1A_GRD', 'S2B_SLC'))
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "(contains(Name,'s1A_GRD') or contains(Name,'S2B_SLC'))"
        )

    def test_mission_filter(self):
        query = query_builder(mission=2)
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "startswith(Name,'S2')"
        )

        query = query_builder(mission=5)
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "startswith(Name,'S5')"
        )

    def test_instrument_filter(self):
        query = query_builder(instrument='MSI')
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "StringAttributes/any(d:d/Name eq "
            "'instrumentShortName' and d/Value eq 'MSI')"
        )

        query = query_builder(instrument='OLCI')
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "StringAttributes/any(d:d/Name eq "
            "'instrumentShortName' and d/Value eq 'OLCI')"
        )

    def test_product_filter(self):
        query = query_builder(product_type='GRD')
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "StringAttributes/any(d:d/Name eq 'productType'"
            " and d/Value eq 'GRD')"
        )

        query = query_builder(product_type='L1B_RA_BD1')
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "StringAttributes/any(d:d/Name eq 'productType'"
            " and d/Value eq 'L1B_RA_BD1')"
        )

    def test_cloud_filter(self):
        query = query_builder(cloud='50')
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "Attributes/OData.CSC.DoubleAttribute/any(d:d/Name eq"
            " 'cloudCover' and d/OData.CSC.DoubleAttribute/Value lt 50)"
        )

        query = query_builder(cloud='25')
        self.assertIsNone(query[1])
        self.assertEqual(
            query[0].evaluate(),
            "Attributes/OData.CSC.DoubleAttribute/any(d:d/Name eq"
            " 'cloudCover' and d/OData.CSC.DoubleAttribute/Value lt 25)"
        )

    def test_order_filter(self):
        query = query_builder(order='ContentLength')
        self.assertIsNone(query[0])
        self.assertEqual(
            query[1][0].evaluate(),
            "ContentLength"
        )
        self.assertEqual(
            query[1][1].evaluate(),
            "asc"
        )

        query = query_builder(order='-ContentLength')
        self.assertEqual(
            query[1][0].evaluate(),
            "ContentLength"
        )
        self.assertEqual(
            query[1][1].evaluate(),
            "desc"
        )
