 # Gibsey Backend Architecture

 ```mermaid
 graph LR
   subgraph Docker Services
     cassandra[Cassandra]
     cassandra_init["Cassandra Init (schema seed)"]
     stargate[Stargate]
     fastapi["FastAPI App<br>(main.py)"]
     embed_load["Embed Loader<br>(embed_load.py)"]
   end

   cassandra_init --> cassandra
   cassandra --> stargate
   fastapi --> cassandra
   fastapi --> stargate
   embed_load --> cassandra
 ```