import React, { useEffect, useState } from 'react';
import Table from 'react-bootstrap/Table';
import Select from 'react-select';
import { tableToJson } from '../HelperFunctions';
function TableInput({ json = {} }) {
    const initialJson = {
        "cisco_templates_avail": [
          "Cisco_Template_1",
          "Cisco_Template_2",
          "Cisco_Template_3",
          "Cisco_Template_4",
          "Cisco_Template_5"
        ],
        "nodes": [
          {
            "node_id": "1",
            "node_name": "Node_1",
            "eve_template": "EVE_Template_1",
            "cisco_target": ""
          },
          {
            "node_id": "2",
            "node_name": "Node_2",
            "eve_template": "EVE_Template_2",
            "cisco_target": "Cisco_Template_2"
          },
          {
            "node_id": "3",
            "node_name": "Node_3",
            "eve_template": "EVE_Template_1",
            "cisco_target": "Cisco_Template_2"
          },
          {
            "node_id": "4",
            "node_name": "Node_4",
            "eve_template": "EVE_Template_3",
            "cisco_target": "Cisco_Template_3"
          },
          {
            "node_id": "5",
            "node_name": "Node_5",
            "eve_template": "EVE_Template_4",
            "cisco_target": ""
          },
          {
            "node_id": "6",
            "node_name": "Node_6",
            "eve_template": "EVE_Template_5",
            "cisco_target": "Cisco_Template_4"
          },
          {
            "node_id": "7",
            "node_name": "Node_7",
            "eve_template": "EVE_Template_1",
            "cisco_target": ""
          },
          {
            "node_id": "8",
            "node_name": "Node_8",
            "eve_template": "EVE_Template_2",
            "cisco_target": "Cisco_Template_1"
          },
          {
            "node_id": "9",
            "node_name": "Node_9",
            "eve_template": "EVE_Template_3",
            "cisco_target": "Cisco_Template_5"
          },
          {
            "node_id": "10",
            "node_name": "Node_10",
            "eve_template": "EVE_Template_4",
            "cisco_target": ""
          }
        ]
      };
      
  const [jsonData, setJsonData] = useState(initialJson);
  const [ciscoTemplatesAvail, set_cisco_templates_avail] = useState(initialJson.cisco_templates_avail)
  useEffect(() => {
    const transformedOptions = initialJson.cisco_templates_avail.map(opt => ({ label: opt, value: opt }));
    set_cisco_templates_avail(transformedOptions);
  }, []);
  const handleTableSubmit = ()=>{
    let table = tableToJson(document.getElementById('the-table'))
    console.log(table)
  }
  const handleSelect = (nodeId, selectedItem) => {
    setJsonData((prevState) => {
      const updatedNodes = prevState.nodes.map((node) => {
        if (node.node_id === nodeId) {
          return { ...node, cisco_target: selectedItem };
        }
        return node;
      });
      return { ...prevState, nodes: updatedNodes };
    });
  };

  return (
    <>
    <Table striped bordered hover id='the-table'>
      <thead>
        <tr>
          <th>NhandleSelecode ID</th>
          <th>Eve Template</th>
          <th>Cisco Target</th>
        </tr>
      </thead>
      <tbody>
        {jsonData.nodes.map((node) => (
          <tr key={node.node_id}>
            <td><p>{node.node_name}</p></td>
            <td><p>{node.eve_template}</p></td>
            <td>
            <Select
  options={ciscoTemplatesAvail}
  value={node.cisco_target ? { label: node.cisco_target, value: node.cisco_target } : null}
  onChange={(selectedItem) => handleSelect(node.node_id, selectedItem)}
/>            </td>
          </tr>
        ))}
      </tbody>
    </Table>
    <div className='d-flex justify-items-end'>
        <button onClick={handleTableSubmit} className='btn btn-primary'>Submit</button>
    </div>
    </>
  );
}

export default TableInput;
