import spacy


class NamedEntityExtractor:
    """
    Performs named entity recognition from texts
    """

    def extract(self, text: str):
        """
        Performs named entity recognition from text
        :param text: Text to extract
        """
        # load spacy nlp library
        spacy_nlp = spacy.load('en_core_web_sm')

        # parse text into spacy document
        doc = spacy_nlp(text.strip())

        # create sets to hold words
        named_entities = set()
        money_entities = set()
        organization_entities = set()
        location_entities = set()
        time_indicator_entities = set()

        for i in doc.ents:
            entry = str(i.lemma_).lower()
            text = text.replace(str(i).lower(), "")
            # Time indicator entities detection
            if i.label_ in ["TIM", "DATE"]:
                time_indicator_entities.add(entry)
            # money value entities detection
            elif i.label_ in ["MONEY"]:
                money_entities.add(entry)
            # organization entities detection
            elif i.label_ in ["ORG"]:
                organization_entities.add(entry)
            # Geographical and Geographical entities detection
            elif i.label_ in ["GPE", "GEO"]:
                location_entities.add(entry)
            # extract artifacts, events and natural phenomenon from text
            elif i.label_ in ["ART", "EVE", "NAT", "PERSON"]:
                named_entities.add(entry.title())

        print(f"named entities - {named_entities}")
        print(f"money entities - {money_entities}")
        print(f"location entities - {location_entities}")
        print(f"time indicator entities - {time_indicator_entities}")
        print(f"organization entities - {organization_entities}")


if __name__ == '__main__':
    named_entity_extractor = NamedEntityExtractor()
    text = "John bought a Toyota camry 2019 model in Toronto in January 2020 at a cost of $38000"
    named_entity_extractor.extract(text)
    text1 = "Larry Anderson, CIBC 8563837"
    named_entity_extractor.extract(text1)
    text2 = "ACC 300019896 GASOLINERA Y SERVICIOS VILLABONITA, S.A. DE C.V."
    named_entity_extractor.extract(text2)
    text3 = "8563837 Canadian Imperial Bank of Commerce, Canada, Larry Anderson,"
    named_entity_extractor.extract(text3)