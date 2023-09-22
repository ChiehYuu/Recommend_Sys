import matplotlib.pyplot as plt
import sqlparse

def parse_sql(sql):
    statements = sqlparse.parse(sql)
    tables = []
    relationships = []
    
    for statement in statements:
        if statement.get_type() == 'CREATE':
            tokens = statement.tokens
            entity_name = None
            attributes = []
            for token in tokens:
                if token.ttype == sqlparse.tokens.Keyword and token.value.upper() == 'TABLE':
                    entity_name = tokens[tokens.index(token) + 2].get_real_name()
                if token.ttype == sqlparse.tokens.Keyword and token.value.upper() == 'FOREIGN':
                    fk_column = tokens[tokens.index(token) + 2].get_real_name()
                    ref_table = tokens[tokens.index(token) + 6].get_real_name()
                    ref_column = tokens[tokens.index(token) + 8].get_real_name()
                    relationships.append((entity_name, ref_table, fk_column, ref_column))
                if token.ttype == sqlparse.tokens.Keyword and token.value.upper() == 'PRIMARY':
                    pk_column = tokens[tokens.index(token) + 6].get_real_name()
                    attributes.append(pk_column)
                if token.ttype == sqlparse.tokens.Name and tokens[tokens.index(token) + 1].value.upper() == 'VARCHAR':
                    attributes.append(token.get_real_name())
            tables.append((entity_name, attributes))
    
    return tables, relationships

def draw_erd(tables, relationships):
    fig, ax = plt.subplots(figsize=(8, 6))
    for table in tables:
        entity_name, attributes = table
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=None, alpha=0))
        ax.text(0.5, 0.9, entity_name, ha='center', va='center', fontsize=12, fontweight='bold')
        for i, attr in enumerate(attributes):
            ax.text(0.1, 0.85 - i * 0.1, attr, ha='left', va='center', fontsize=10)
    
    for relationship in relationships:
        entity1, entity2, attr1, attr2 = relationship
        ax.arrow(0.5, 0.2, 0, -0.1, head_width=0.05, head_length=0.1, fc='blue', ec='blue')
        ax.text(0.5, 0.15, f'{attr1} -> {attr2}', ha='center', va='center', fontsize=10, color='blue')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.show()

if __name__ == "__main__":
    sql = """
    CREATE TABLE Customer (
        customer_id INT PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50)
    );

    CREATE TABLE Order (
        order_id INT PRIMARY KEY,
        order_date DATE,
        customer_id INT,
        FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
    );
    """
    tables, relationships = parse_sql(sql)
    draw_erd(tables, relationships)