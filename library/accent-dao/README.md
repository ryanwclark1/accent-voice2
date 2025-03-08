### Data Access Object/Layer

- [ ] Evaluate tradeoffs for async and look at upgrade
- [ ] Restructure tests

  A Data Access Object (DAO) is a pattern that provides an abstract interface to the SQLAlchemy Object Relational Mapper (ORM). The DAOs are critical as they form the building block of the application which are wrapped by the associated commands and RESTful API endpoints.

Currently there are numerous inconsistencies and violation of the DRY principal within the codebase as it relates to DAOs and ORMs—unnecessary commits, non-ACID transactions, etc.—which makes the code unnecessarily complex and convoluted. Addressing the underlying issues with the DAOs should help simplify the downstream operations and improve the developer experience.

To ensure consistency the following rules should be adhered to:

All database operations (including testing) should be defined within a DAO, i.e., there should not be any explicit db.session.add, db.session.merge, etc. calls outside of a DAO.
A DAO should use create, update, delete, upsert terms—typical database operations which ensure consistency with commands—rather than action based terms like save, saveas, override, etc.
Sessions should be managed via a context manager which auto-commits on success and rolls back on failure, i.e., there should be no explicit db.session.commit or db.session.rollback calls within the DAO.
There should be a single atomic transaction representing the entirety of the operation, i.e., when creating a dataset with associated columns and metrics either all the changes succeed when the transaction is committed, or all the changes are undone when the transaction is rolled back. SQLAlchemy supports nested transactions via the begin_nested method which can be nested—inline with how DAOs are invoked.
The database layer should adopt a "shift left" mentality i.e., uniqueness/foreign key constraints, relationships, cascades, etc. should all be defined in the underlying database schema where possible. Note there are times where this isn’t possible, i.e., MySQL and PostgreSQL treat NULL values differently from a uniqueness perspective. If modeled correctly the ORM should implicitly delete all associations and thus one should not need to preemptively undefine relationships, etc.
Avoid validation logic, i.e., ask for forgiveness rather than permission. This is akin to a try/except block where the exception is the exception rather than the rule. Thus instead of first checking whether something is defined before adding, simply try adding it (and per 5) and rely on the database to verify whether the model is acceptable. This removes potential race conditions, reduces the number of database operations, and reduces the code footprint.
Provide bulk create, update, delete, etc. methods (if possible) for performance reasons.
By default updates should be sparse in nature, i.e., only those attributes which are explicitly defined are updated.
Tests should leverage nested transactions which should be rolled back on teardown. This is cleaner than deleting objects. See here for details.
