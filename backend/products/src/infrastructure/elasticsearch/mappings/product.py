PRODUCT_INDEX_MAPPING = {
    "settings": {
        "analysis": {
            "filter": {
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "edge_ngram_3_15": {
                    "type": "edge_ngram",
                    "min_gram": 3,
                    "max_gram": 15
                },
                "synonym_filter": {
                    "type": "synonym",
                    "synonyms": [
                        "кроссовки, кеды, sneakers",
                        "телефон, смартфон, phone"
                    ]
                }
            },
            "analyzer": {
                "bilingual": {
                    "type": "custom",
                    "tokenizer": "icu_tokenizer",
                    "filter": [
                        "icu_folding",
                        "lowercase",
                        "russian_stop",
                        "english_stop",
                        "russian_stemmer",
                        "english_stemmer",
                        "synonym_filter"
                    ]
                },
                "edge_ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "edge_ngram_3_15"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "name": {
                "type": "text",
                "analyzer": "bilingual",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    },
                    "edge": {
                        "type": "text",
                        "analyzer": "edge_ngram_analyzer"
                    }
                }
            },
            "brand": {
                "type": "text",
                "analyzer": "bilingual",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    },
                    "edge": {
                        "type": "text",
                        "analyzer": "edge_ngram_analyzer"
                    }
                }
            },
            "supplier_id": {"type": "integer"},
            "average_rating": {"type": "float"},
            "review_count": {"type": "integer"},
            "price": {"type": "scaled_float", "scaling_factor": 100},
            "quantity": {"type": "integer"},
            "category_id": {"type": "integer"},
            "status": {"type": "keyword"},
            "variants": {
                "type": "nested",
                "properties": {
                    "size": {"type": "keyword"},
                    "color": {"type": "keyword"},
                    "stock": {"type": "integer"}
                }
            }
        }
    }
}