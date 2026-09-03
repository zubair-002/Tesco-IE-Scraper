import time
from random import uniform

import requests

headers = {
    'accept': 'application/json',
    'accept-language': 'en-IE',
    'content-type': 'application/json',
    'language': 'en-IE',
    'origin': 'https://www.tesco.ie',
    'priority': 'u=1, i',
    'referer': 'https://www.tesco.ie/shop/en-IE/buylists/top-picks/summer-hosting?count=24&page=2',
    'region': 'IE',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'traceid': 'a0ebc9ce-21c3-4382-996e-8330dc4ca45d:0d98f005-906e-4443-8f48-b2c0ba8fde2c',
    'trkid': 'a0ebc9ce-21c3-4382-996e-8330dc4ca45d',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-apikey': 'TvOSZJHlEk0pjniDGQFAc9Q59WGAR4dA',
}


def get_payload(id, page):
    return [
        {
            'operationName': 'GetCategoryProducts',
            'variables': {
                'page': page,
                'includeRestrictions': True,
                'includeVariations': True,
                'showDepositReturnCharge': True,
                'count': 27,
                'facet': id,
                'configs': [
                    {
                        'featureKey': 'dynamic_filter',
                        'params': [
                            {
                                'name': 'enable',
                                'value': 'true',
                            },
                        ],
                    },
                ],
                'filterCriteria': [
                    {
                        'name': '0',
                        'values': [
                            'groceries',
                        ],
                    },
                ],
                'appliedFacetArgs': [],
                'sortBy': 'relevance',
            },
            'extensions': {
                'mfeName': 'mfe-plp',
            },
            'query': 'query GetCategoryProducts($facet: ID, $page: Int = 1, $count: Int, $sortBy: String, $offset: Int, $favourites: Boolean, $configs: [ConfigArgType], $filterCriteria: [filterCriteria], $includeRestrictions: Boolean = true, $includeVariations: Boolean = true, $mediaExperiments: BrowseSearchConfig, $showDepositReturnCharge: Boolean = false, $appliedFacetArgs: [AppliedFacetArgs]) {\n  category(\n    page: $page\n    count: $count\n    configs: $configs\n    sortBy: $sortBy\n    offset: $offset\n    facet: $facet\n    favourites: $favourites\n    config: $mediaExperiments\n    filterCriteria: $filterCriteria\n    appliedFacetArgs: $appliedFacetArgs\n  ) {\n    pageInformation: info {\n      ...PageInformation\n      __typename\n    }\n    results {\n      node {\n        ... on MPProduct {\n          ...ProductItem\n          __typename\n        }\n        ... on FNFProduct {\n          ...ProductItem\n          __typename\n        }\n        ... on ProductType {\n          ...ProductItem\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    facetLists: facetGroups {\n      ...FacetLists\n      __typename\n    }\n    facets {\n      ...facet\n      __typename\n    }\n    options {\n      sortBy\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProductItem on ProductInterface {\n  typename: __typename\n  ... on ProductType {\n    context {\n      type\n      ... on ProductContextOfferType {\n        linkTo\n        offerType\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  sellers(type: TOP, limit: 1, offset: 0) {\n    ...Sellers\n    __typename\n  }\n  ... on MPProduct {\n    context {\n      type\n      ... on ProductContextOfferType {\n        linkTo\n        offerType\n        __typename\n      }\n      __typename\n    }\n    seller {\n      id\n      name\n      __typename\n    }\n    variations {\n      ...Variation @include(if: $includeVariations)\n      __typename\n    }\n    __typename\n  }\n  ... on FNFProduct {\n    context {\n      type\n      ... on ProductContextOfferType {\n        linkTo\n        offerType\n        __typename\n      }\n      __typename\n    }\n    variations {\n      priceRange {\n        minPrice\n        maxPrice\n        __typename\n      }\n      ...Variation @include(if: $includeVariations)\n      __typename\n    }\n    __typename\n  }\n  id\n  tpnb\n  tpnc\n  gtin\n  adId\n  baseProductId\n  title\n  brandName\n  shortDescription\n  defaultImageUrl\n  superDepartmentId\n  media {\n    defaultImage {\n      aspectRatio\n      __typename\n    }\n    __typename\n  }\n  quantityInBasket\n  superDepartmentName\n  departmentId\n  departmentName\n  aisleId\n  aisleName\n  shelfId\n  shelfName\n  displayType\n  productType\n  charges @include(if: $showDepositReturnCharge) {\n    ... on ProductDepositReturnCharge {\n      __typename\n      amount\n    }\n    __typename\n  }\n  averageWeight\n  bulkBuyLimit\n  maxQuantityAllowed: bulkBuyLimit\n  groupBulkBuyLimit\n  bulkBuyLimitMessage\n  bulkBuyLimitGroupId\n  timeRestrictedDelivery\n  restrictedDelivery\n  isInFavourites\n  isNew\n  isRestrictedOrderAmendment\n  maxWeight\n  minWeight\n  increment\n  details {\n    components {\n      ...Competitors\n      ...AdditionalInfo\n      __typename\n    }\n    __typename\n  }\n  catchWeightList {\n    price\n    weight\n    default\n    __typename\n  }\n  restrictions @include(if: $includeRestrictions) {\n    type\n    isViolated\n    message\n    __typename\n  }\n  reviews {\n    stats {\n      noOfReviews\n      overallRating\n      overallRatingRange\n      __typename\n    }\n    __typename\n  }\n  modelMetadata {\n    name\n    version\n    __typename\n  }\n}\n\nfragment Competitors on CompetitorsInfo {\n  competitors {\n    id\n    priceMatch {\n      isMatching\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment AdditionalInfo on AdditionalInfo {\n  isLowEverydayPricing\n  __typename\n}\n\nfragment Variation on VariationsType {\n  products {\n    id\n    baseProductId\n    variationAttributes {\n      attributeGroup\n      attributeGroupData {\n        name\n        value\n        attributes {\n          name\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Sellers on ProductSellers {\n  __typename\n  results {\n    id\n    __typename\n    isForSale\n    status\n    seller {\n      id\n      name\n      logo {\n        url\n        __typename\n      }\n      __typename\n    }\n    price {\n      price: actual\n      unitPrice\n      unitOfMeasure\n      actual\n      __typename\n    }\n    promotions {\n      id\n      promotionType\n      startDate\n      endDate\n      description\n      unitSellingInfo\n      price {\n        beforeDiscount\n        afterDiscount\n        __typename\n      }\n      attributes\n      __typename\n    }\n    fulfilment(deliveryOptions: BEST) {\n      __typename\n      ... on ProductDeliveryType {\n        end\n        charges {\n          value\n          __typename\n        }\n        __typename\n      }\n    }\n  }\n}\n\nfragment FacetLists on ProductListFacetsType {\n  __typename\n  category\n  categoryId\n  facets {\n    facetId: id\n    facetName: name\n    binCount: count\n    isSelected: selected\n    __typename\n  }\n}\n\nfragment PageInformation on ListInfoType {\n  totalCount: total\n  pageNo: page\n  pageId\n  count\n  pageSize\n  matchType\n  offset\n  query {\n    searchTerm\n    actualTerm\n    queryPhase\n    __typename\n  }\n  __typename\n}\n\nfragment facet on FacetInterface {\n  __typename\n  id\n  name\n  type\n  ... on FacetListType {\n    id\n    name\n    listValues: values {\n      name\n      value\n      isSelected\n      count\n      __typename\n    }\n    multiplicity\n    metadata {\n      description\n      footerText\n      linkText\n      linkUrl\n      __typename\n    }\n    __typename\n  }\n  ... on FacetMultiLevelType {\n    id\n    name\n    multiLevelValues: values {\n      children {\n        count\n        name\n        value\n        isSelected\n        __typename\n      }\n      appliedValues {\n        isSelected\n        name\n        value\n        __typename\n      }\n      __typename\n    }\n    multiplicity\n    metadata {\n      description\n      footerText\n      linkText\n      linkUrl\n      __typename\n    }\n    __typename\n  }\n  ... on FacetBooleanType {\n    booleanValues: values {\n      count\n      isSelected\n      value\n      name\n      __typename\n    }\n    __typename\n  }\n}\n',
        },

    ]


json_data = [
    {
        'operationName': 'Taxonomy',
        'variables': {
            'includeInspirationEvents': True,
        },
        'extensions': {
            'mfeName': 'mfe-plp',
        },
        'query': 'query Taxonomy($storeId: ID, $includeInspirationEvents: Boolean = true, $deliveryType: DeliveryTypeEnum, $configs: [ConfigArgType]) {\n  taxonomy: taxonomy(\n    storeId: $storeId\n    includeInspirationEvents: $includeInspirationEvents\n    deliveryType: $deliveryType\n    configs: $configs\n  ) {\n    ...taxon\n    children {\n      ...taxon\n      children {\n        ...taxon\n        children {\n          ...taxon\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment taxon on TaxonomyItemInterface {\n  __typename\n  catId: id\n  name\n  label\n  parent\n  pageType\n  images(style: "thumbnail") {\n    __typename\n    style\n    images {\n      __typename\n      type\n      url\n    }\n  }\n}\n',
    },
]

# response = requests.post('https://xapi.tesco.com/', headers=headers, json=json_data)

# SKIP_NAMES = {'Marketplace'}
# MarketPlace = False
# THRESHOLD = 10000
# print("Getting Category IDs ---")

# def has_marketplace_image(node):
#     """Return True if any thumbnail image url on this node contains 'marketplace'."""
#     for image_group in node.get('images') or []:
#         for image in image_group.get('images') or []:
#             url = image.get('url') or ''
#             if 'marketplace' in url.lower():
#                 return True
#     return False

# ids = []
# under_threshold = []     
# drilled_into = []       
# kept_no_children = []    


# def get_total_count(cat_id):
#     """Call the API for this facet id and return pageInformation.totalCount, or None on failure."""
#     payload = get_payload(cat_id, 1)
#     resp = requests.post('https://xapi.tesco.com/', headers=headers, json=payload)
#     resp_data = resp.json()
#     page_info = resp_data[0]['data']['category']['pageInformation']
#     return page_info['totalCount']


# def process_node(node, depth=0):
#     if node.get('name') in SKIP_NAMES:
#         return

#     cat_id = node.get('catId')
#     name = node.get('name', '')

#     if not cat_id or 'www.tesco.com' in cat_id:
#         return
#     if has_marketplace_image(node) != MarketPlace:
#         return

#     try:
#         total = get_total_count(cat_id)
#     except Exception as e:
#         print(f"{'  ' * depth}!! Failed to fetch count for '{name}' ({cat_id}): {e}")
#         return

#     print(f"{'  ' * depth}{name}")

#     children = node.get('children') or []

#     if total < THRESHOLD:
#         ids.append(cat_id)
#         under_threshold.append((name, cat_id, total))
#     elif children:
#         drilled_into.append((name, cat_id, total))
#         for child in children:
#             process_node(child, depth + 1)
#             time.sleep(1)  # Sleep for 0.5 seconds between processing child nodes
#     else:
#         kept_no_children.append((name, cat_id, total))

# data = response.json()[0]
# for taxonomy in data['data']['taxonomy'][1:]:
#     process_node(taxonomy)
#     time.sleep(3)  # Sleep for 3 seconds between processing top-level taxonomy nodes


# print(f"\n{len(ids)} total facet IDs selected.\n")
