# Bluesky followers graph computation

We have G = (V, E) with V = {all the users from Bluesky} and E : {v -> u, v follows u}.

We want to compute the list E.

# Fileformats

Every vertice is represented by an integer ID, of a length of 4 bytes.

`*.edges` : (4 bytes, 4 bytes)*, representing the ID of the follower, the ID of the followed
`*.mappings` : Some mappings in the form (4bytes, str terminated by \0,)*
    NOTE : Each slave should only export the nodes it has assigned