{
    "name" : "Real Estate Ads",
    "version" : "1.0",
    "website" : "https//www.jivika.com",
    "author" : "jivika",
    "description" : """
        Real Estate module to show available properties
        """,
    "category" : "Sales",
    "depends" : [],
    "data" : [
        'security/ir.model.access.csv',
        'views/property_view.xml',
        'views/property_type.xml',
        'views/property_tag.xml',
        'views/property_offer_view.xml',
        'views/menuitems.xml',

        #'data/property_type.xml',
        'data/estate.property.type.csv',

        
    ],

    'demo': [
        'demo/property_tag.xml'
    ],
    "installable" : True,
    "application" : True,
    "license" : "LGPL-3"
}