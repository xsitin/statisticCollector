class Company:
    def __init__(self, company_name, group_id, ):
        self.company_name = company_name
        self.group_id = group_id

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"""company_name:{self.company_name}
        group_id:{self.group_id}"""

