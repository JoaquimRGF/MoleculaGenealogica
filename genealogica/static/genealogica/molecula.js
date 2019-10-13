    // A practical solution (covering all browsers):
    var w = window.innerWidth
    || document.documentElement.clientWidth
    || document.body.clientWidth;

    var h = window.innerHeight
    || document.documentElement.clientHeight
    || document.body.clientHeight;

    var nodes_total = [];
    var links_total = [];

    d3.json("http://127.0.0.1:8000/api/person/?format=json").then(function(json) {
    nodes_total = json;

    d3.json("http://127.0.0.1:8000/api/links/?format=json").then(function(json) {
      {for (i = 0; i < json.length; i++) {
      {for (j = 0; j < json[i].data.length; j++) {
        links_total.push(json[i].data[j])}};
    }};


    // Definition of body and svg
    // Definition of zoom and remove double click to zoom
    var vis1 = d3.select("body").append("svg:svg").attr("width", w).attr("height", h).call(d3.zoom()
    .scaleExtent([.1, 4])
    .on("zoom", function () {vis.attr("transform", d3.event.transform);}))
    .on("dblclick.zoom", null);

    var vis = vis1.append("g");

    var selected = null;

    // Credits to https://bl.ocks.org/mapio/53fed7d84cd1812d6a6639ed7aa83868

    // first definition of filtered nodes (no filter)
    var nodes = nodes_total
    var links = links_total

    // defition of a dictionary to map id of node to index
    var nodesbyid = {}
    for (var i = 0; i < nodes_total.length; i++) {
      nodesbyid[
        nodes_total[i]["id"]] = i
    }

    // adjency lists to help verification of neighbors
    var adjlist = {};
    for (var i = 0; i < links_total.length; i++) {
      adjlist[nodesbyid[links_total[i].source] + "-" + nodesbyid[links_total[i].target]] = true;
      adjlist[nodesbyid[links_total[i].target] + "-" + nodesbyid[links_total[i].source]] = true;
      links_total[i].source = nodesbyid[links_total[i].source];
      links_total[i]["id"] = i;
      links_total[i].target = nodesbyid[links_total[i].target];
    };



    // Initialization of D3 Force Simulation
    var labelLayout = d3.forceSimulation()
      .force("charge", d3.forceManyBody().strength(-60))

    var graphLayout = d3.forceSimulation()
      .force("charge", d3.forceManyBody().strength(-3000))
      .force("center", d3.forceCenter(w / 2, h / 2))
      .force("x", d3.forceX(w / 2).strength(1))
      .force("y", d3.forceY(h / 2).strength(1))

    
    // Defition of drag 
    var node_drag = d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);

    // Initialization of SVG Elements 
    var linkElements = vis.append("g")
      .attr("class", "links")
      .selectAll("line")

    var nodeElements = vis.append("g")
      .attr("class", "nodes")
      .selectAll("circle")


    var labelNode = vis.append("g").attr("class", "labelNodes")
      .selectAll("text")

    // Function that produces the svg per se-
    update()

    
    function update() {

      // Definition of label of nodes
      var label = {
        'nodes': [],
        'links': []
      };

      nodes.forEach(function (d, i) {
        label.nodes.push({ node: d, id: d.id * 2 });
        label.nodes.push({ node: d, id: d.id * 2 + 1 });
        label.links.push({
          source: i * 2,
          target: i * 2 + 1,
          id: i * 2
        });
      });

      // Remove elements that are eliminated by filter
      linkElements = linkElements.data(links, function (d) { return d.id; });
      linkElements.exit().remove();

      // Insert new elements
      var newlinkElements = linkElements.enter().append("line")
        .attr("stroke-width", 5)
        .attr("stroke", function (d) { return colorstandartlink(d) });
      
      // Update elements 
      linkElements = linkElements.merge(newlinkElements)

      // Remove elements that are eliminated by filter
      nodeElements = nodeElements.data(nodes, function (d) { return d.id; });
      nodeElements.exit().remove();

      // Insert new elements
      var newnodeElements = nodeElements.enter().append("circle")
        .attr("r", 12)
        .attr("fill", getNodeColor) // Color nodes
        .on('click', selectNode) // Select Node
        .on("dblclick", dblclick) // Add neighbords in filtered views
        .on("contextmenu", lftclick) // Remove fixed position
        .call(node_drag) // Allow drag of node

      // Update elements 
      nodeElements = nodeElements.merge(newnodeElements)

      // Allow Focus of nodes
      nodeElements.on("mouseover", focus).on("mouseout", unfocus);



      // Remove elements that are eliminated by filter
      labelNode = labelNode.data(label.nodes, function (d) { return d.id; });
      labelNode.exit().remove();


      // Insert new elements
      var newlabelNode = labelNode.enter()
        .append("text")
        .text(function (d, i) { return i % 2 == 0 ? "" : d.node.name; })
        .style("fill", "#555")
        .style("font-family", "Arial")
        .style("font-size", 12)
        .style("pointer-events", "none"); // to prevent mouseover/drag capture. This means that you cannot copy text (unless you go to the console)


      // Update elements 
      labelNode = labelNode.merge(newlabelNode)


      // Define nodes and links in the graph and restart force simulation 
      graphLayout.nodes(nodes);
      graphLayout.force("link", d3.forceLink(links).id(function (d) { return d.index; }).distance(50).strength(1))
      graphLayout.on("tick", ticked)
      graphLayout.restart();

      // Define label nodes and links in the graph and restart force simulation
      labelLayout.nodes(label.nodes);
      labelLayout.force("link", d3.forceLink(label.links).distance(10).strength(2));
      labelLayout.on("tick", ticked)
      labelLayout.restart();
    }

    // Function that defines the location of each element in the SVG
    function ticked() {
      // Define location of Nodes 
      nodeElements.call(updateNode);
      // Define location of Links 
      linkElements.call(updateLink);

      // Define location of Label Nodes 
      labelLayout.alphaTarget(0.3).restart();
      labelNode.each(function (d, i) {
        if (i % 2 == 0) {
          // If node on the left of the screen push the label to the left of the node
          if (d.node.x < w / 2) {
            d.x = d.node.x - Math.min(d.node.name.length * 11 * (w / 2 - d.node.x) / (w / 2), d.node.name.length * 5)
          } else {
            d.x = d.node.x + Math.min(d.node.name.length * 7 * (w / 2 - d.node.x) / (w / 2), d.node.name.length * 5);
          }

          d.y = d.node.y;
        } else {
          var b = this.getBBox();

          var diffX = d.x - d.node.x;
          var diffY = d.y - d.node.y;

          var dist = Math.sqrt(diffX * diffX + diffY * diffY);

          var shiftX = b.width * (diffX - dist) / (dist * 2);
          shiftX = Math.max(-b.width, Math.min(0, shiftX));
          var shiftY = 16;
          this.setAttribute("transform", "translate(" + shiftX + "," + shiftY + ")");
        }
      });
      labelNode.call(updateNode);

    }

    // Search for unions
    function getUnion(node) {
      return links.reduce(function (union, link) {
        if (link.type === "union" && (link.target.id === node.id || link.source.id === node.id)) {
          union.push(link.target.id)
        }
        return union
      },
        [node.id]
      )
    }

    // Function that retrieve children of node
    function getChildren(node) {
      return links.reduce(function (children, link) {
        if (link.source.id === node.id && link.type === "children") {
          children.push(link.target.id)
        }
        return children
      },
        []
      )
    }

    // Function that retrieve parents of node
    function getParents(node) {
      return links.reduce(function (parents, link) {
        if (link.target.id === node.id && link.type === "children") {
          parents.push(link.source.id)
        }
        return parents
      },
        []
      )
    }

    // Function that indicates if a link is of a specified node
    function isNeighborLink(node, link) {
      if (node === null) {
        return false;
      }
      return link.target.id === node.id || link.source.id === node.id
    }

    // Function that colors nodes
    function getNodeColor(node, union, children, parents) {
      if (Array.isArray(union) && Array.isArray(children) && Array.isArray(parents)) {
        return union.indexOf(node.id) > -1 ? '#fbb831' : '#689ba5' && children.indexOf(node.id) > -1 ? '#5bc8c1' : '#689ba5' && parents.indexOf(node.id) > -1 ? '#aaba6a' : '#689ba5'
      } else { return '#689ba5' }
    }


    // Standard colors of links
    function colorstandartlink(link) {
      if (link.type === 'union') {
        return "#e08080";
      } else {
        return "rgba(50, 50, 50, 0.2)";
      }
    }

    // Function that colors links
    function getLinkColor(node, link) {
      if (isNeighborLink(node, link)) {
        if (link.type === 'union') {
          return "#e08080";
        }
        else {
          return "#aaba6a"
        }
      }
      else {
        return colorstandartlink(link)
      }
    }

    // Function that colors text
    function getTextColor(node, union, children, parents) {
      if (Array.isArray(union) && Array.isArray(children) && Array.isArray(parents)) {
        return union.indexOf(node.id) > -1 ? '#fbb831' : 'black' && children.indexOf(node.id) > -1 ? '#aaba6a' : 'black' && parents.indexOf(node.id) > -1 ? '#aaba6a' : 'black'
      } else {
        return "black";
      }
    }

    // Function that selects a node and colors its neighborhood
    function selectNode(selectedNode) {
      if (selected === selectedNode) {
        selected = null;
        var union = null;
        var children = null;
        var parents = null;
        // we modify the styles to undo highlight
        nodeElements.attr('fill', function (node) { return getNodeColor(node, union, children, parents) })
        // nodeElements.label.style('fill', function (node) { return getTextColor(node, union, children, parents) })
        linkElements.attr('stroke', function (link) { return getLinkColor(selected, link) })
      } else {
        var union = getUnion(selectedNode);
        var children = getChildren(selectedNode);
        var parents = getParents(selectedNode);
        // we modify the styles to highlight selected nodes
        nodeElements.attr('fill', function (node) { return getNodeColor(node, union, children, parents) })
        // nodeElements.label.style('fill', function (node) { return getTextColor(node, union, children, parents) })
        linkElements.attr('stroke', function (link) { return getLinkColor(selectedNode, link) })
        selected = selectedNode;
      }
    }

    // Function that retrieves the data from the input text form and applies a automatic filter
    var input = document.querySelector('#search-node');
    if (input) {
      input.addEventListener('input', function () {
        if (input.value === "" || !input.value) {
          nodes = nodes_total
          links = links_total
        } else {
          // Filter nodes
          var aux = regex_search(nodes_total, input.value)
          nodes = aux[0]
          var nodes_ids = aux[1]
          // nodes, nodes_ids = regex_search(nodes_total, input.value)
          // Retrieve links of given nodes
          links = filter_links_by_nodes(links_total, nodes_ids)
        }
        // Update graph
        update()
      });
    }


    // Regex search through nodes names
    function regex_search(nodes_list, search_string) {
      let re = new RegExp(search_string, "ig");
      let new_nodes = []
      let new_nodes_ids = []
      for (var i = 0; i < nodes_list.length; i++) {
        if (nodes_list[i].name.search(re) > -1) {
          new_nodes.push(nodes_list[i])
          new_nodes_ids.push(nodes_list[i].id)
        }
      }
      return [new_nodes, new_nodes_ids]
    }

    // Search of links of given nodes ids
    function filter_links_by_nodes(links_list, nodes_list) {
      let new_list = links_list.filter(function (link) {
        if (nodes_list.includes(link.source.id) && nodes_list.includes(link.target.id)) {
          return true
        }
        else {
          return false
        }
      })
      return new_list
    }

    // On double click add neighbor nodes if not present and respective links
    function dblclick(d) {
      var index = d3.select(d3.event.target).datum().id;
      let new_nodes_ids = nodes.map(function (node) { return node.id })
      for (var i = 0; i < nodes_total.length; i++) {
        if (!new_nodes_ids.includes(nodes_total[i].id) && neigh(nodesbyid[index], nodesbyid[nodes_total[i].id])) {
          nodes.push(nodes_total[i])

          new_nodes_ids.push(nodes_total[i].id)
        }
      }
      links = filter_links_by_nodes(links_total, new_nodes_ids)
      update()
    }

    // Remove the fixed position of a node after drag 
    function lftclick(d, i) {
      d3.event.preventDefault();
      if (d.fixed) {
        d.fx = null;
        d.fy = null;
        d3.select(this).classed("fixed", d.fixed = false);
      }
    }

    // Start Drag of node
    function dragstarted(d) {
      d3.event.sourceEvent.stopPropagation();
      if (!d3.event.active) graphLayout.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    // middle of drag 
    function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }

    // End drag of node
    function dragended(d) {
      if (!d3.event.active) graphLayout.alphaTarget(0);
      d.fixed = true;
    }

    // Function that indicated if two node index are neighbors
    function neigh(a, b) {
      return a == b || adjlist[a + "-" + b];
    }

    // Function that compensated overflow and Nan
    function fixna(x) {
      if (isFinite(x)) return x;
      return 0;
    }

    // Function that highlights neighbor nodes and links
    function focus(d) {
      var index = d3.select(d3.event.target).datum().index;
      nodeElements.style("opacity", function (o) {
        return neigh(index, o.index) ? 1 : 0.1;
      });
      labelNode.attr("display", function (o) {
        return neigh(index, o.node.index) ? "block" : "none";
      });
      linkElements.style("opacity", function (o) {
        return o.source.index == index || o.target.index == index ? 1 : 0.1;
      });
    }

    // Remove focus of node
    function unfocus() {
      labelNode.attr("display", "block");
      nodeElements.style("opacity", 1);
      linkElements.style("opacity", 1);
    }

    // Update position of links
    function updateLink(link) {
      link.attr("x1", function (d) { return fixna(d.source.x); })
        .attr("y1", function (d) { return fixna(d.source.y); })
        .attr("x2", function (d) { return fixna(d.target.x); })
        .attr("y2", function (d) { return fixna(d.target.y); });
    }
    // Update position of nodes
    function updateNode(node) {
      node.attr("transform", function (d) {
        return "translate(" + fixna(d.x) + "," + fixna(d.y) + ")";
      });
    }
    });
    });