window.SWMM_HTML_CONTRACT = {
  "version": "2026-06-12-swmm-first-contract-v1",
  "sourceOfTruth": "SWMM",
  "modelPath": "/Users/onseoktae/Documents/swmm/models/seoul_rebuild_v2.inp",
  "viewerRole": "render_only_with_controls",
  "controlBoundary": {
    "htmlCanControl": [
      "rainfall",
      "object_blockage"
    ],
    "htmlMustNotCalculate": [
      "hydraulic_flow",
      "backflow",
      "fullness",
      "pump_discharge"
    ],
    "pythonBridgeRole": "advance_pyswmm_step_and_return_state"
  },
  "swmmIndexes": {
    "nodes": {
      "road_runoff_sep_catch_basin_1": {
        "id": "road_runoff_sep_catch_basin_1",
        "nodeType": "JUNCTION",
        "elevationM": 12.2,
        "maxDepthM": 0.35,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.4,
        "pondedAreaM2": 18.0,
        "map": {
          "x": 1195.0,
          "y": 1654.0
        }
      },
      "road_runoff_sep_catch_basin_2": {
        "id": "road_runoff_sep_catch_basin_2",
        "nodeType": "JUNCTION",
        "elevationM": 12.2,
        "maxDepthM": 0.35,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.4,
        "pondedAreaM2": 18.0,
        "map": {
          "x": 1985.0,
          "y": 1654.0
        }
      },
      "sep_apartment_1": {
        "id": "sep_apartment_1",
        "nodeType": "JUNCTION",
        "elevationM": 11.35,
        "maxDepthM": 1.0,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 245.0,
          "y": 1682.0
        }
      },
      "sep_apartment_2": {
        "id": "sep_apartment_2",
        "nodeType": "JUNCTION",
        "elevationM": 11.3,
        "maxDepthM": 1.0,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 847.0,
          "y": 1682.0
        }
      },
      "sep_sewer_lateral_apartment_1_elbow_connector": {
        "id": "sep_sewer_lateral_apartment_1_elbow_connector",
        "nodeType": "JUNCTION",
        "elevationM": 11.33,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 365.0,
          "y": 1682.0
        }
      },
      "sep_sewer_lateral_apartment_2_elbow_connector": {
        "id": "sep_sewer_lateral_apartment_2_elbow_connector",
        "nodeType": "JUNCTION",
        "elevationM": 11.28,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 727.0,
          "y": 1682.0
        }
      },
      "sep_sewer_upstream": {
        "id": "sep_sewer_upstream",
        "nodeType": "JUNCTION",
        "elevationM": 8.7,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 0.0,
          "y": 1075.0
        }
      },
      "sep_sewer_main_1_apartment_1_connector": {
        "id": "sep_sewer_main_1_apartment_1_connector",
        "nodeType": "JUNCTION",
        "elevationM": 8.55,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 365.0,
          "y": 1075.0
        }
      },
      "sep_sewer_manhole": {
        "id": "sep_sewer_manhole",
        "nodeType": "JUNCTION",
        "elevationM": 8.45,
        "maxDepthM": 3.6,
        "initialDepthM": 0.0,
        "surchargeDepthM": 1.2,
        "pondedAreaM2": 20.0,
        "map": {
          "x": 546.0,
          "y": 1075.0
        }
      },
      "sep_sewer_main_2_apartment_2_connector": {
        "id": "sep_sewer_main_2_apartment_2_connector",
        "nodeType": "JUNCTION",
        "elevationM": 8.35,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 727.0,
          "y": 1075.0
        }
      },
      "sep_sewer_downstream": {
        "id": "sep_sewer_downstream",
        "nodeType": "JUNCTION",
        "elevationM": 8.1,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2170.0,
          "y": 1075.0
        }
      },
      "sep_sewer_main_to_interceptor_elbow_connector": {
        "id": "sep_sewer_main_to_interceptor_elbow_connector",
        "nodeType": "JUNCTION",
        "elevationM": 8.07,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2264.0,
          "y": 1075.0
        }
      },
      "sep_interceptor_upstream": {
        "id": "sep_interceptor_upstream",
        "nodeType": "JUNCTION",
        "elevationM": 6.55,
        "maxDepthM": 3.2,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.8,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 0.0,
          "y": 231.0
        }
      },
      "sep_interceptor_join": {
        "id": "sep_interceptor_join",
        "nodeType": "JUNCTION",
        "elevationM": 6.2,
        "maxDepthM": 3.2,
        "initialDepthM": 0.0,
        "surchargeDepthM": 1.0,
        "pondedAreaM2": 20.0,
        "map": {
          "x": 2264.0,
          "y": 231.0
        }
      },
      "overflow_interceptor_join": {
        "id": "overflow_interceptor_join",
        "nodeType": "JUNCTION",
        "elevationM": 5.65,
        "maxDepthM": 3.2,
        "initialDepthM": 0.0,
        "surchargeDepthM": 1.0,
        "pondedAreaM2": 20.0,
        "map": {
          "x": 4753.0,
          "y": 231.0
        }
      },
      "sep_interceptor_downstream": {
        "id": "sep_interceptor_downstream",
        "nodeType": "JUNCTION",
        "elevationM": 5.6,
        "maxDepthM": 3.2,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.8,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 4978.0,
          "y": 231.0
        }
      },
      "treatment_process_outlet_node": {
        "id": "treatment_process_outlet_node",
        "nodeType": "JUNCTION",
        "elevationM": 4.95,
        "maxDepthM": 3.2,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.8,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 5578.0,
          "y": 223.0
        }
      },
      "treated_outfall_gate_node": {
        "id": "treated_outfall_gate_node",
        "nodeType": "JUNCTION",
        "elevationM": 4.86,
        "maxDepthM": 3.2,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.8,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 5870.0,
          "y": 223.0
        }
      },
      "sep_storm_lateral_catch_basin_1_start": {
        "id": "sep_storm_lateral_catch_basin_1_start",
        "nodeType": "JUNCTION",
        "elevationM": 11.33,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 1250.0,
          "y": 1586.0
        }
      },
      "sep_storm_lateral_catch_basin_1_elbow_connector": {
        "id": "sep_storm_lateral_catch_basin_1_elbow_connector",
        "nodeType": "JUNCTION",
        "elevationM": 11.31,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 1370.0,
          "y": 1586.0
        }
      },
      "sep_storm_lateral_catch_basin_2_start": {
        "id": "sep_storm_lateral_catch_basin_2_start",
        "nodeType": "JUNCTION",
        "elevationM": 11.33,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2040.0,
          "y": 1586.0
        }
      },
      "sep_storm_lateral_catch_basin_2_elbow_connector": {
        "id": "sep_storm_lateral_catch_basin_2_elbow_connector",
        "nodeType": "JUNCTION",
        "elevationM": 11.31,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2160.0,
          "y": 1586.0
        }
      },
      "sep_storm_main_1_catch_basin_1_connector": {
        "id": "sep_storm_main_1_catch_basin_1_connector",
        "nodeType": "JUNCTION",
        "elevationM": 8.75,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 30.0,
        "map": {
          "x": 1370.0,
          "y": 1370.0
        }
      },
      "offscreen_catch_basin_storm_main_1": {
        "id": "offscreen_catch_basin_storm_main_1",
        "nodeType": "JUNCTION",
        "elevationM": 8.95,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 0.0,
          "y": 1370.0
        }
      },
      "sep_storm_manhole": {
        "id": "sep_storm_manhole",
        "nodeType": "JUNCTION",
        "elevationM": 8.65,
        "maxDepthM": 3.55,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 50.0,
        "map": {
          "x": 1704.0,
          "y": 1370.0
        }
      },
      "sep_storm_main_2_catch_basin_2_connector": {
        "id": "sep_storm_main_2_catch_basin_2_connector",
        "nodeType": "JUNCTION",
        "elevationM": 8.38,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 30.0,
        "map": {
          "x": 2160.0,
          "y": 1370.0
        }
      },
      "sep_storm_main_2_outlet_connector": {
        "id": "sep_storm_main_2_outlet_connector",
        "nodeType": "JUNCTION",
        "elevationM": 8.32,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 50.0,
        "map": {
          "x": 2240.0,
          "y": 1370.0
        }
      },
      "sep_storm_main_to_trunk_elbow_connector": {
        "id": "sep_storm_main_to_trunk_elbow_connector",
        "nodeType": "JUNCTION",
        "elevationM": 8.29,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 50.0,
        "map": {
          "x": 2355.0,
          "y": 1370.0
        }
      },
      "sep_storm_trunk_upstream": {
        "id": "sep_storm_trunk_upstream",
        "nodeType": "JUNCTION",
        "elevationM": 6.16,
        "maxDepthM": 3.0,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 0.0,
          "y": 766.0
        }
      },
      "sep_storm_trunk_main_2_drop_connector": {
        "id": "sep_storm_trunk_main_2_drop_connector",
        "nodeType": "JUNCTION",
        "elevationM": 5.6,
        "maxDepthM": 3.0,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2355.0,
          "y": 766.0
        }
      },
      "sep_storm_trunk_downstream": {
        "id": "sep_storm_trunk_downstream",
        "nodeType": "JUNCTION",
        "elevationM": 5.01,
        "maxDepthM": 3.0,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 4800.0,
          "y": 766.0
        }
      },
      "storm_pump_inlet_gate_node": {
        "id": "storm_pump_inlet_gate_node",
        "nodeType": "JUNCTION",
        "elevationM": 4.95,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 4885.0,
          "y": 762.0
        }
      },
      "storm_pump_discharge_node": {
        "id": "storm_pump_discharge_node",
        "nodeType": "JUNCTION",
        "elevationM": 5.2,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 5400.0,
          "y": 761.0
        }
      },
      "pump_outfall_gate_node": {
        "id": "pump_outfall_gate_node",
        "nodeType": "JUNCTION",
        "elevationM": 5.03,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 5870.0,
          "y": 761.0
        }
      },
      "road_runoff_offscreen_comb_catch_basin": {
        "id": "road_runoff_offscreen_comb_catch_basin",
        "nodeType": "JUNCTION",
        "elevationM": 12.2,
        "maxDepthM": 0.35,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.4,
        "pondedAreaM2": 18.0,
        "map": {
          "x": 2440.0,
          "y": 1654.0
        }
      },
      "offscreen_comb_sewer_source": {
        "id": "offscreen_comb_sewer_source",
        "nodeType": "JUNCTION",
        "elevationM": 8.88,
        "maxDepthM": 1.2,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.4,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2440.0,
          "y": 1262.0
        }
      },
      "offscreen_comb_storm_lateral_start": {
        "id": "offscreen_comb_storm_lateral_start",
        "nodeType": "JUNCTION",
        "elevationM": 11.33,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2480.0,
          "y": 1586.0
        }
      },
      "offscreen_comb_storm_lateral_elbow_connector": {
        "id": "offscreen_comb_storm_lateral_elbow_connector",
        "nodeType": "JUNCTION",
        "elevationM": 11.31,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2510.0,
          "y": 1586.0
        }
      },
      "comb_upstream": {
        "id": "comb_upstream",
        "nodeType": "JUNCTION",
        "elevationM": 8.82,
        "maxDepthM": 2.6,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2440.0,
          "y": 1223.0
        }
      },
      "comb_house_1": {
        "id": "comb_house_1",
        "nodeType": "JUNCTION",
        "elevationM": 11.1,
        "maxDepthM": 1.0,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2645.0,
          "y": 1682.0
        }
      },
      "comb_sewer_lateral_house_1_elbow_connector": {
        "id": "comb_sewer_lateral_house_1_elbow_connector",
        "nodeType": "JUNCTION",
        "elevationM": 11.08,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2850.0,
          "y": 1682.0
        }
      },
      "comb_main_house_1_connector": {
        "id": "comb_main_house_1_connector",
        "nodeType": "JUNCTION",
        "elevationM": 8.6,
        "maxDepthM": 2.6,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 2850.0,
          "y": 1223.0
        }
      },
      "comb_house_2": {
        "id": "comb_house_2",
        "nodeType": "JUNCTION",
        "elevationM": 11.0,
        "maxDepthM": 1.0,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 3075.0,
          "y": 1682.0
        }
      },
      "comb_sewer_lateral_house_2_elbow_connector": {
        "id": "comb_sewer_lateral_house_2_elbow_connector",
        "nodeType": "JUNCTION",
        "elevationM": 10.98,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 3280.0,
          "y": 1682.0
        }
      },
      "comb_main_house_2_connector": {
        "id": "comb_main_house_2_connector",
        "nodeType": "JUNCTION",
        "elevationM": 8.54,
        "maxDepthM": 2.6,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 3280.0,
          "y": 1223.0
        }
      },
      "road_runoff_comb_catch_basin_1": {
        "id": "road_runoff_comb_catch_basin_1",
        "nodeType": "JUNCTION",
        "elevationM": 12.2,
        "maxDepthM": 0.35,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.4,
        "pondedAreaM2": 18.0,
        "map": {
          "x": 3475.0,
          "y": 1654.0
        }
      },
      "comb_storm_lateral_catch_basin_1_start": {
        "id": "comb_storm_lateral_catch_basin_1_start",
        "nodeType": "JUNCTION",
        "elevationM": 11.33,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 3530.0,
          "y": 1586.0
        }
      },
      "comb_storm_lateral_catch_basin_1_elbow_connector": {
        "id": "comb_storm_lateral_catch_basin_1_elbow_connector",
        "nodeType": "JUNCTION",
        "elevationM": 11.31,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 3650.0,
          "y": 1586.0
        }
      },
      "comb_main_catch_basin_1_connector": {
        "id": "comb_main_catch_basin_1_connector",
        "nodeType": "JUNCTION",
        "elevationM": 8.43,
        "maxDepthM": 2.6,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 3650.0,
          "y": 1223.0
        }
      },
      "combined_manhole": {
        "id": "combined_manhole",
        "nodeType": "JUNCTION",
        "elevationM": 8.35,
        "maxDepthM": 3.5,
        "initialDepthM": 0.0,
        "surchargeDepthM": 1.2,
        "pondedAreaM2": 20.0,
        "map": {
          "x": 3900.0,
          "y": 1223.0
        }
      },
      "road_runoff_comb_catch_basin_2": {
        "id": "road_runoff_comb_catch_basin_2",
        "nodeType": "JUNCTION",
        "elevationM": 12.2,
        "maxDepthM": 0.35,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.4,
        "pondedAreaM2": 18.0,
        "map": {
          "x": 4225.0,
          "y": 1654.0
        }
      },
      "comb_storm_lateral_catch_basin_2_start": {
        "id": "comb_storm_lateral_catch_basin_2_start",
        "nodeType": "JUNCTION",
        "elevationM": 11.28,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 4280.0,
          "y": 1586.0
        }
      },
      "comb_storm_lateral_catch_basin_2_elbow_connector": {
        "id": "comb_storm_lateral_catch_basin_2_elbow_connector",
        "nodeType": "JUNCTION",
        "elevationM": 11.26,
        "maxDepthM": 0.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.3,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 4400.0,
          "y": 1586.0
        }
      },
      "comb_main_catch_basin_2_connector": {
        "id": "comb_main_catch_basin_2_connector",
        "nodeType": "JUNCTION",
        "elevationM": 8.18,
        "maxDepthM": 2.6,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 4400.0,
          "y": 1223.0
        }
      },
      "overflow_normal_flow_node": {
        "id": "overflow_normal_flow_node",
        "nodeType": "JUNCTION",
        "elevationM": 7.62,
        "maxDepthM": 2.8,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 4753.0,
          "y": 1054.0
        }
      },
      "overflow_weir_outlet_node": {
        "id": "overflow_weir_outlet_node",
        "nodeType": "JUNCTION",
        "elevationM": 7.7,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 5012.0,
          "y": 1223.0
        }
      },
      "overflow_outfall_gate_node": {
        "id": "overflow_outfall_gate_node",
        "nodeType": "JUNCTION",
        "elevationM": 6.3,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "surchargeDepthM": 0.5,
        "pondedAreaM2": 0.0,
        "map": {
          "x": 5870.0,
          "y": 1223.0
        }
      },
      "sep_catch_basin_1": {
        "id": "sep_catch_basin_1",
        "nodeType": "STORAGE",
        "elevationM": 11.0,
        "maxDepthM": 1.2,
        "initialDepthM": 0.0,
        "shape": "FUNCTIONAL",
        "storageParam": 2.0,
        "map": {
          "x": 1195.0,
          "y": 1576.0
        }
      },
      "sep_catch_basin_2": {
        "id": "sep_catch_basin_2",
        "nodeType": "STORAGE",
        "elevationM": 11.0,
        "maxDepthM": 1.2,
        "initialDepthM": 0.0,
        "shape": "FUNCTIONAL",
        "storageParam": 2.0,
        "map": {
          "x": 1985.0,
          "y": 1576.0
        }
      },
      "offscreen_comb_catch_basin": {
        "id": "offscreen_comb_catch_basin",
        "nodeType": "STORAGE",
        "elevationM": 11.0,
        "maxDepthM": 1.2,
        "initialDepthM": 0.0,
        "shape": "FUNCTIONAL",
        "storageParam": 2.0,
        "map": {
          "x": 2440.0,
          "y": 1576.0
        }
      },
      "comb_catch_basin_1": {
        "id": "comb_catch_basin_1",
        "nodeType": "STORAGE",
        "elevationM": 11.0,
        "maxDepthM": 1.2,
        "initialDepthM": 0.0,
        "shape": "FUNCTIONAL",
        "storageParam": 2.0,
        "map": {
          "x": 3475.0,
          "y": 1576.0
        }
      },
      "comb_catch_basin_2": {
        "id": "comb_catch_basin_2",
        "nodeType": "STORAGE",
        "elevationM": 10.95,
        "maxDepthM": 1.2,
        "initialDepthM": 0.0,
        "shape": "FUNCTIONAL",
        "storageParam": 2.0,
        "map": {
          "x": 4225.0,
          "y": 1576.0
        }
      },
      "overflow_chamber": {
        "id": "overflow_chamber",
        "nodeType": "STORAGE",
        "elevationM": 7.75,
        "maxDepthM": 2.8,
        "initialDepthM": 0.0,
        "shape": "FUNCTIONAL",
        "storageParam": 45.0,
        "map": {
          "x": 4752.0,
          "y": 1220.0
        }
      },
      "storm_pump_station": {
        "id": "storm_pump_station",
        "nodeType": "STORAGE",
        "elevationM": 4.7,
        "maxDepthM": 2.4,
        "initialDepthM": 0.0,
        "shape": "FUNCTIONAL",
        "storageParam": 25.0,
        "map": {
          "x": 5092.0,
          "y": 762.0
        }
      },
      "water_reclamation_center": {
        "id": "water_reclamation_center",
        "nodeType": "STORAGE",
        "elevationM": 5.05,
        "maxDepthM": 4.0,
        "initialDepthM": 0.15,
        "shape": "FUNCTIONAL",
        "storageParam": 120.0,
        "map": {
          "x": 5270.0,
          "y": 228.0
        }
      },
      "overflow_outfall": {
        "id": "overflow_outfall",
        "nodeType": "OUTFALL",
        "elevationM": 6.25,
        "outfallType": "FREE",
        "gated": "NO",
        "map": {
          "x": 6028.0,
          "y": 1223.0
        }
      },
      "pump_outfall": {
        "id": "pump_outfall",
        "nodeType": "OUTFALL",
        "elevationM": 5.02,
        "outfallType": "FREE",
        "gated": "NO",
        "map": {
          "x": 6054.0,
          "y": 761.0
        }
      },
      "treated_outfall": {
        "id": "treated_outfall",
        "nodeType": "OUTFALL",
        "elevationM": 4.85,
        "outfallType": "FREE",
        "gated": "NO",
        "map": {
          "x": 6028.0,
          "y": 223.0
        }
      }
    },
    "links": {
      "sep_sewer_lateral_apartment_1_horizontal": {
        "id": "sep_sewer_lateral_apartment_1_horizontal",
        "linkType": "CONDUIT",
        "fromNode": "sep_apartment_1",
        "toNode": "sep_sewer_lateral_apartment_1_elbow_connector",
        "lengthM": 18.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001111
      },
      "sep_sewer_lateral_apartment_1_vertical": {
        "id": "sep_sewer_lateral_apartment_1_vertical",
        "linkType": "CONDUIT",
        "fromNode": "sep_sewer_lateral_apartment_1_elbow_connector",
        "toNode": "sep_sewer_main_1_apartment_1_connector",
        "lengthM": 30.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.2,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.092667
      },
      "sep_sewer_lateral_apartment_2_horizontal": {
        "id": "sep_sewer_lateral_apartment_2_horizontal",
        "linkType": "CONDUIT",
        "fromNode": "sep_apartment_2",
        "toNode": "sep_sewer_lateral_apartment_2_elbow_connector",
        "lengthM": 18.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001111
      },
      "sep_sewer_lateral_apartment_2_vertical": {
        "id": "sep_sewer_lateral_apartment_2_vertical",
        "linkType": "CONDUIT",
        "fromNode": "sep_sewer_lateral_apartment_2_elbow_connector",
        "toNode": "sep_sewer_main_2_apartment_2_connector",
        "lengthM": 30.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.2,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.097667
      },
      "sep_sewer_main_1_upstream_segment": {
        "id": "sep_sewer_main_1_upstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "sep_sewer_upstream",
        "toNode": "sep_sewer_main_1_apartment_1_connector",
        "lengthM": 185.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.05,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.000811
      },
      "sep_sewer_main_1_downstream_segment": {
        "id": "sep_sewer_main_1_downstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "sep_sewer_main_1_apartment_1_connector",
        "toNode": "sep_sewer_manhole",
        "lengthM": 45.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.05,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.002222
      },
      "sep_sewer_main_2_upstream_segment": {
        "id": "sep_sewer_main_2_upstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "sep_sewer_manhole",
        "toNode": "sep_sewer_main_2_apartment_2_connector",
        "lengthM": 60.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.05,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001667
      },
      "sep_sewer_main_2_downstream_segment": {
        "id": "sep_sewer_main_2_downstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "sep_sewer_main_2_apartment_2_connector",
        "toNode": "sep_sewer_downstream",
        "lengthM": 200.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.05,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.00125
      },
      "sep_sewer_main_to_interceptor_horizontal": {
        "id": "sep_sewer_main_to_interceptor_horizontal",
        "linkType": "CONDUIT",
        "fromNode": "sep_sewer_downstream",
        "toNode": "sep_sewer_main_to_interceptor_elbow_connector",
        "lengthM": 24.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.05,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.00125
      },
      "sep_sewer_main_to_interceptor_vertical": {
        "id": "sep_sewer_main_to_interceptor_vertical",
        "linkType": "CONDUIT",
        "fromNode": "sep_sewer_main_to_interceptor_elbow_connector",
        "toNode": "sep_interceptor_join",
        "lengthM": 40.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.05,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.5,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.04675
      },
      "sep_interceptor_upstream_segment": {
        "id": "sep_interceptor_upstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "sep_interceptor_upstream",
        "toNode": "sep_interceptor_join",
        "lengthM": 460.0,
        "roughnessN": 0.016,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.000761
      },
      "sep_interceptor_join_to_overflow_segment": {
        "id": "sep_interceptor_join_to_overflow_segment",
        "linkType": "CONDUIT",
        "fromNode": "sep_interceptor_join",
        "toNode": "overflow_interceptor_join",
        "lengthM": 570.0,
        "roughnessN": 0.016,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.000965
      },
      "sep_interceptor_downstream_segment": {
        "id": "sep_interceptor_downstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "overflow_interceptor_join",
        "toNode": "sep_interceptor_downstream",
        "lengthM": 50.0,
        "roughnessN": 0.016,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001
      },
      "sep_interceptor_to_reclamation_inlet": {
        "id": "sep_interceptor_to_reclamation_inlet",
        "linkType": "CONDUIT",
        "fromNode": "sep_interceptor_downstream",
        "toNode": "water_reclamation_center",
        "lengthM": 45.0,
        "roughnessN": 0.016,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.012222
      },
      "treatment_process_limited_outlet": {
        "id": "treatment_process_limited_outlet",
        "linkType": "CONDUIT",
        "fromNode": "water_reclamation_center",
        "toNode": "treatment_process_outlet_node",
        "lengthM": 30.0,
        "roughnessN": 0.014,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.02,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.2,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.003333
      },
      "treatment_effluent_pipe": {
        "id": "treatment_effluent_pipe",
        "linkType": "CONDUIT",
        "fromNode": "treatment_process_outlet_node",
        "toNode": "treated_outfall_gate_node",
        "lengthM": 300.0,
        "roughnessN": 0.014,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.0003
      },
      "sep_storm_lateral_catch_basin_1_horizontal": {
        "id": "sep_storm_lateral_catch_basin_1_horizontal",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_lateral_catch_basin_1_start",
        "toNode": "sep_storm_lateral_catch_basin_1_elbow_connector",
        "lengthM": 18.0,
        "roughnessN": 0.018,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001111
      },
      "sep_storm_lateral_catch_basin_1_vertical": {
        "id": "sep_storm_lateral_catch_basin_1_vertical",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_lateral_catch_basin_1_elbow_connector",
        "toNode": "sep_storm_main_1_catch_basin_1_connector",
        "lengthM": 30.0,
        "roughnessN": 0.018,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.2,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.085333
      },
      "sep_storm_lateral_catch_basin_2_horizontal": {
        "id": "sep_storm_lateral_catch_basin_2_horizontal",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_lateral_catch_basin_2_start",
        "toNode": "sep_storm_lateral_catch_basin_2_elbow_connector",
        "lengthM": 18.0,
        "roughnessN": 0.018,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001111
      },
      "sep_storm_lateral_catch_basin_2_vertical": {
        "id": "sep_storm_lateral_catch_basin_2_vertical",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_lateral_catch_basin_2_elbow_connector",
        "toNode": "sep_storm_main_2_catch_basin_2_connector",
        "lengthM": 30.0,
        "roughnessN": 0.018,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.2,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.097667
      },
      "sep_storm_main_1_upstream_segment": {
        "id": "sep_storm_main_1_upstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "offscreen_catch_basin_storm_main_1",
        "toNode": "sep_storm_main_1_catch_basin_1_connector",
        "lengthM": 175.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.2,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001143
      },
      "sep_storm_main_1_downstream_segment": {
        "id": "sep_storm_main_1_downstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_main_1_catch_basin_1_connector",
        "toNode": "sep_storm_manhole",
        "lengthM": 85.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.2,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001176
      },
      "sep_storm_main_2_upstream_segment": {
        "id": "sep_storm_main_2_upstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_manhole",
        "toNode": "sep_storm_main_2_catch_basin_2_connector",
        "lengthM": 233.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.2,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001159
      },
      "sep_storm_main_2_downstream_segment": {
        "id": "sep_storm_main_2_downstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_main_2_catch_basin_2_connector",
        "toNode": "sep_storm_main_2_outlet_connector",
        "lengthM": 47.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.2,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001277
      },
      "sep_storm_main_to_trunk_horizontal": {
        "id": "sep_storm_main_to_trunk_horizontal",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_main_2_outlet_connector",
        "toNode": "sep_storm_main_to_trunk_elbow_connector",
        "lengthM": 24.0,
        "roughnessN": 0.016,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.00125
      },
      "sep_storm_main_to_trunk_vertical": {
        "id": "sep_storm_main_to_trunk_vertical",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_main_to_trunk_elbow_connector",
        "toNode": "sep_storm_trunk_main_2_drop_connector",
        "lengthM": 40.0,
        "roughnessN": 0.016,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.5,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.06725
      },
      "sep_storm_trunk_upstream_segment": {
        "id": "sep_storm_trunk_upstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_trunk_upstream",
        "toNode": "sep_storm_trunk_main_2_drop_connector",
        "lengthM": 490.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001143
      },
      "sep_storm_trunk_downstream_segment": {
        "id": "sep_storm_trunk_downstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_trunk_main_2_drop_connector",
        "toNode": "sep_storm_trunk_downstream",
        "lengthM": 510.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001157
      },
      "sep_storm_trunk_to_pump_station": {
        "id": "sep_storm_trunk_to_pump_station",
        "linkType": "CONDUIT",
        "fromNode": "sep_storm_trunk_downstream",
        "toNode": "storm_pump_inlet_gate_node",
        "lengthM": 35.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001714
      },
      "storm_pump_discharge_pipe": {
        "id": "storm_pump_discharge_pipe",
        "linkType": "CONDUIT",
        "fromNode": "storm_pump_discharge_node",
        "toNode": "pump_outfall_gate_node",
        "lengthM": 145.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001172
      },
      "offscreen_comb_sewer_lateral": {
        "id": "offscreen_comb_sewer_lateral",
        "linkType": "CONDUIT",
        "fromNode": "offscreen_comb_sewer_source",
        "toNode": "comb_upstream",
        "lengthM": 24.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.0025
      },
      "offscreen_comb_storm_lateral_horizontal": {
        "id": "offscreen_comb_storm_lateral_horizontal",
        "linkType": "CONDUIT",
        "fromNode": "offscreen_comb_storm_lateral_start",
        "toNode": "offscreen_comb_storm_lateral_elbow_connector",
        "lengthM": 18.0,
        "roughnessN": 0.018,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001111
      },
      "offscreen_comb_storm_lateral_vertical": {
        "id": "offscreen_comb_storm_lateral_vertical",
        "linkType": "CONDUIT",
        "fromNode": "offscreen_comb_storm_lateral_elbow_connector",
        "toNode": "comb_upstream",
        "lengthM": 30.0,
        "roughnessN": 0.018,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.2,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.083
      },
      "comb_sewer_lateral_house_1_horizontal": {
        "id": "comb_sewer_lateral_house_1_horizontal",
        "linkType": "CONDUIT",
        "fromNode": "comb_house_1",
        "toNode": "comb_sewer_lateral_house_1_elbow_connector",
        "lengthM": 18.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001111
      },
      "comb_sewer_lateral_house_1_vertical": {
        "id": "comb_sewer_lateral_house_1_vertical",
        "linkType": "CONDUIT",
        "fromNode": "comb_sewer_lateral_house_1_elbow_connector",
        "toNode": "comb_main_house_1_connector",
        "lengthM": 30.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.2,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.082667
      },
      "comb_sewer_lateral_house_2_horizontal": {
        "id": "comb_sewer_lateral_house_2_horizontal",
        "linkType": "CONDUIT",
        "fromNode": "comb_house_2",
        "toNode": "comb_sewer_lateral_house_2_elbow_connector",
        "lengthM": 18.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001111
      },
      "comb_sewer_lateral_house_2_vertical": {
        "id": "comb_sewer_lateral_house_2_vertical",
        "linkType": "CONDUIT",
        "fromNode": "comb_sewer_lateral_house_2_elbow_connector",
        "toNode": "comb_main_house_2_connector",
        "lengthM": 30.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.2,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.081333
      },
      "comb_storm_lateral_catch_basin_1_horizontal": {
        "id": "comb_storm_lateral_catch_basin_1_horizontal",
        "linkType": "CONDUIT",
        "fromNode": "comb_storm_lateral_catch_basin_1_start",
        "toNode": "comb_storm_lateral_catch_basin_1_elbow_connector",
        "lengthM": 18.0,
        "roughnessN": 0.018,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001111
      },
      "comb_storm_lateral_catch_basin_1_vertical": {
        "id": "comb_storm_lateral_catch_basin_1_vertical",
        "linkType": "CONDUIT",
        "fromNode": "comb_storm_lateral_catch_basin_1_elbow_connector",
        "toNode": "comb_main_catch_basin_1_connector",
        "lengthM": 30.0,
        "roughnessN": 0.018,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.2,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.096
      },
      "comb_storm_lateral_catch_basin_2_horizontal": {
        "id": "comb_storm_lateral_catch_basin_2_horizontal",
        "linkType": "CONDUIT",
        "fromNode": "comb_storm_lateral_catch_basin_2_start",
        "toNode": "comb_storm_lateral_catch_basin_2_elbow_connector",
        "lengthM": 18.0,
        "roughnessN": 0.018,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001111
      },
      "comb_storm_lateral_catch_basin_2_vertical": {
        "id": "comb_storm_lateral_catch_basin_2_vertical",
        "linkType": "CONDUIT",
        "fromNode": "comb_storm_lateral_catch_basin_2_elbow_connector",
        "toNode": "comb_main_catch_basin_2_connector",
        "lengthM": 30.0,
        "roughnessN": 0.018,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.2,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.102667
      },
      "comb_main_1_upstream_segment": {
        "id": "comb_main_1_upstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "comb_upstream",
        "toNode": "comb_main_house_1_connector",
        "lengthM": 220.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.2,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001
      },
      "comb_main_1_house_1_to_house_2_segment": {
        "id": "comb_main_1_house_1_to_house_2_segment",
        "linkType": "CONDUIT",
        "fromNode": "comb_main_house_1_connector",
        "toNode": "comb_main_house_2_connector",
        "lengthM": 60.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.2,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001
      },
      "comb_main_1_house_2_to_catch_basin_1_segment": {
        "id": "comb_main_1_house_2_to_catch_basin_1_segment",
        "linkType": "CONDUIT",
        "fromNode": "comb_main_house_2_connector",
        "toNode": "comb_main_catch_basin_1_connector",
        "lengthM": 110.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.2,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001
      },
      "comb_main_1_to_manhole_segment": {
        "id": "comb_main_1_to_manhole_segment",
        "linkType": "CONDUIT",
        "fromNode": "comb_main_catch_basin_1_connector",
        "toNode": "combined_manhole",
        "lengthM": 80.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.2,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001
      },
      "comb_main_2_manhole_to_catch_basin_2_segment": {
        "id": "comb_main_2_manhole_to_catch_basin_2_segment",
        "linkType": "CONDUIT",
        "fromNode": "combined_manhole",
        "toNode": "comb_main_catch_basin_2_connector",
        "lengthM": 120.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.2,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.001417
      },
      "comb_main_2_downstream_segment": {
        "id": "comb_main_2_downstream_segment",
        "linkType": "CONDUIT",
        "fromNode": "comb_main_catch_basin_2_connector",
        "toNode": "overflow_chamber",
        "lengthM": 70.0,
        "roughnessN": 0.015,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.2,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.006143
      },
      "overflow_to_interceptor_drop": {
        "id": "overflow_to_interceptor_drop",
        "linkType": "CONDUIT",
        "fromNode": "overflow_normal_flow_node",
        "toNode": "overflow_interceptor_join",
        "lengthM": 40.0,
        "roughnessN": 0.016,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.95,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 1.5,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.04925
      },
      "overflow_pipe": {
        "id": "overflow_pipe",
        "linkType": "CONDUIT",
        "fromNode": "overflow_weir_outlet_node",
        "toNode": "overflow_outfall_gate_node",
        "lengthM": 280.0,
        "roughnessN": 0.016,
        "inOffsetM": 0.0,
        "outOffsetM": 0.0,
        "initialFlowCms": 0.0,
        "maxFlowCms": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        },
        "losses": {
          "inletLoss": 0.0,
          "outletLoss": 0.0,
          "averageLoss": 0.0,
          "flapGate": "NO",
          "seepageRate": 0.0
        },
        "computedSlope": 0.005
      },
      "sep_catch_basin_1_inlet_connector": {
        "id": "sep_catch_basin_1_inlet_connector",
        "linkType": "ORIFICE",
        "fromNode": "road_runoff_sep_catch_basin_1",
        "toNode": "sep_catch_basin_1",
        "orificeType": "BOTTOM",
        "offsetM": 0.0,
        "qCoeff": 0.65,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "RECT_CLOSED",
          "geom1": 0.6,
          "geom2": 0.6,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "sep_catch_basin_1_outlet_connector": {
        "id": "sep_catch_basin_1_outlet_connector",
        "linkType": "ORIFICE",
        "fromNode": "sep_catch_basin_1",
        "toNode": "sep_storm_lateral_catch_basin_1_start",
        "orificeType": "SIDE",
        "offsetM": 0.33,
        "qCoeff": 0.65,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "sep_catch_basin_2_inlet_connector": {
        "id": "sep_catch_basin_2_inlet_connector",
        "linkType": "ORIFICE",
        "fromNode": "road_runoff_sep_catch_basin_2",
        "toNode": "sep_catch_basin_2",
        "orificeType": "BOTTOM",
        "offsetM": 0.0,
        "qCoeff": 0.65,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "RECT_CLOSED",
          "geom1": 0.6,
          "geom2": 0.6,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "sep_catch_basin_2_outlet_connector": {
        "id": "sep_catch_basin_2_outlet_connector",
        "linkType": "ORIFICE",
        "fromNode": "sep_catch_basin_2",
        "toNode": "sep_storm_lateral_catch_basin_2_start",
        "orificeType": "SIDE",
        "offsetM": 0.33,
        "qCoeff": 0.65,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "storm_pump_inlet_gate": {
        "id": "storm_pump_inlet_gate",
        "linkType": "ORIFICE",
        "fromNode": "storm_pump_inlet_gate_node",
        "toNode": "storm_pump_station",
        "orificeType": "SIDE",
        "offsetM": 0.0,
        "qCoeff": 0.75,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "pump_outfall_gate": {
        "id": "pump_outfall_gate",
        "linkType": "ORIFICE",
        "fromNode": "pump_outfall_gate_node",
        "toNode": "pump_outfall",
        "orificeType": "SIDE",
        "offsetM": 0.0,
        "qCoeff": 0.75,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "treated_outfall_gate": {
        "id": "treated_outfall_gate",
        "linkType": "ORIFICE",
        "fromNode": "treated_outfall_gate_node",
        "toNode": "treated_outfall",
        "orificeType": "SIDE",
        "offsetM": 0.0,
        "qCoeff": 0.75,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "offscreen_comb_catch_basin_inlet_connector": {
        "id": "offscreen_comb_catch_basin_inlet_connector",
        "linkType": "ORIFICE",
        "fromNode": "road_runoff_offscreen_comb_catch_basin",
        "toNode": "offscreen_comb_catch_basin",
        "orificeType": "BOTTOM",
        "offsetM": 0.0,
        "qCoeff": 0.65,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "RECT_CLOSED",
          "geom1": 0.6,
          "geom2": 0.6,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "offscreen_comb_catch_basin_outlet_connector": {
        "id": "offscreen_comb_catch_basin_outlet_connector",
        "linkType": "ORIFICE",
        "fromNode": "offscreen_comb_catch_basin",
        "toNode": "offscreen_comb_storm_lateral_start",
        "orificeType": "SIDE",
        "offsetM": 0.33,
        "qCoeff": 0.65,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "comb_catch_basin_1_inlet_connector": {
        "id": "comb_catch_basin_1_inlet_connector",
        "linkType": "ORIFICE",
        "fromNode": "road_runoff_comb_catch_basin_1",
        "toNode": "comb_catch_basin_1",
        "orificeType": "BOTTOM",
        "offsetM": 0.0,
        "qCoeff": 0.65,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "RECT_CLOSED",
          "geom1": 0.6,
          "geom2": 0.6,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "comb_catch_basin_1_outlet_connector": {
        "id": "comb_catch_basin_1_outlet_connector",
        "linkType": "ORIFICE",
        "fromNode": "comb_catch_basin_1",
        "toNode": "comb_storm_lateral_catch_basin_1_start",
        "orificeType": "SIDE",
        "offsetM": 0.33,
        "qCoeff": 0.65,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "comb_catch_basin_2_inlet_connector": {
        "id": "comb_catch_basin_2_inlet_connector",
        "linkType": "ORIFICE",
        "fromNode": "road_runoff_comb_catch_basin_2",
        "toNode": "comb_catch_basin_2",
        "orificeType": "BOTTOM",
        "offsetM": 0.0,
        "qCoeff": 0.65,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "RECT_CLOSED",
          "geom1": 0.6,
          "geom2": 0.6,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "comb_catch_basin_2_outlet_connector": {
        "id": "comb_catch_basin_2_outlet_connector",
        "linkType": "ORIFICE",
        "fromNode": "comb_catch_basin_2",
        "toNode": "comb_storm_lateral_catch_basin_2_start",
        "orificeType": "SIDE",
        "offsetM": 0.33,
        "qCoeff": 0.65,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.45,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "overflow_normal_flow_gate": {
        "id": "overflow_normal_flow_gate",
        "linkType": "ORIFICE",
        "fromNode": "overflow_chamber",
        "toNode": "overflow_normal_flow_node",
        "orificeType": "SIDE",
        "offsetM": 0.2,
        "qCoeff": 0.65,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 0.95,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "overflow_outfall_gate": {
        "id": "overflow_outfall_gate",
        "linkType": "ORIFICE",
        "fromNode": "overflow_outfall_gate_node",
        "toNode": "overflow_outfall",
        "orificeType": "SIDE",
        "offsetM": 0.0,
        "qCoeff": 0.75,
        "gated": "NO",
        "closeTimeSec": 0.0,
        "crossSection": {
          "shape": "CIRCULAR",
          "geom1": 1.8,
          "geom2": 0.0,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "overflow_excess_weir": {
        "id": "overflow_excess_weir",
        "linkType": "WEIR",
        "fromNode": "overflow_chamber",
        "toNode": "overflow_weir_outlet_node",
        "weirType": "TRANSVERSE",
        "crestHeightM": 1.6,
        "qCoeff": 1.84,
        "gated": "NO",
        "crossSection": {
          "shape": "RECT_OPEN",
          "geom1": 1.0,
          "geom2": 2.4,
          "geom3": 0.0,
          "geom4": 0.0,
          "barrels": 1,
          "culvert": 0
        }
      },
      "storm_pump_unit": {
        "id": "storm_pump_unit",
        "linkType": "PUMP",
        "fromNode": "storm_pump_station",
        "toNode": "storm_pump_discharge_node",
        "pumpCurve": "STORM_PUMP_CURVE",
        "initialStatus": "OFF",
        "startupDepthM": 0.8,
        "shutoffDepthM": 0.25
      }
    }
  },
  "visualObjects": [
    {
      "htmlId": "sep_apartment_1",
      "label": "분류식 아파트 1",
      "objectType": "surface",
      "system": "separate",
      "waterType": "sewer",
      "swmmNodes": [
        "sep_apartment_1"
      ],
      "swmmLinks": [],
      "controls": {
        "rainfall": false,
        "blockage": false
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_apartment_1",
          "nodeType": "JUNCTION",
          "elevationM": 11.35,
          "maxDepthM": 1.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 245.0,
            "y": 1682.0
          }
        }
      ],
      "resolvedLinks": []
    },
    {
      "htmlId": "sep_apartment_2",
      "label": "분류식 아파트 2",
      "objectType": "surface",
      "system": "separate",
      "waterType": "sewer",
      "swmmNodes": [
        "sep_apartment_2"
      ],
      "swmmLinks": [],
      "controls": {
        "rainfall": false,
        "blockage": false
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_apartment_2",
          "nodeType": "JUNCTION",
          "elevationM": 11.3,
          "maxDepthM": 1.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 847.0,
            "y": 1682.0
          }
        }
      ],
      "resolvedLinks": []
    },
    {
      "htmlId": "sep_catch_basin_1",
      "label": "분류식 빗물받이 1",
      "objectType": "catch_basin",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "road_runoff_sep_catch_basin_1",
        "sep_catch_basin_1"
      ],
      "swmmLinks": [
        "sep_catch_basin_1_inlet_connector"
      ],
      "controls": {
        "rainfall": true,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "road_runoff_sep_catch_basin_1",
          "nodeType": "JUNCTION",
          "elevationM": 12.2,
          "maxDepthM": 0.35,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.4,
          "pondedAreaM2": 18.0,
          "map": {
            "x": 1195.0,
            "y": 1654.0
          }
        },
        {
          "id": "sep_catch_basin_1",
          "nodeType": "STORAGE",
          "elevationM": 11.0,
          "maxDepthM": 1.2,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 2.0,
          "map": {
            "x": 1195.0,
            "y": 1576.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_catch_basin_1_inlet_connector",
          "linkType": "ORIFICE",
          "fromNode": "road_runoff_sep_catch_basin_1",
          "toNode": "sep_catch_basin_1",
          "orificeType": "BOTTOM",
          "offsetM": 0.0,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "RECT_CLOSED",
            "geom1": 0.6,
            "geom2": 0.6,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        }
      ]
    },
    {
      "htmlId": "sep_catch_basin_2",
      "label": "분류식 빗물받이 2",
      "objectType": "catch_basin",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "road_runoff_sep_catch_basin_2",
        "sep_catch_basin_2"
      ],
      "swmmLinks": [
        "sep_catch_basin_2_inlet_connector"
      ],
      "controls": {
        "rainfall": true,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "road_runoff_sep_catch_basin_2",
          "nodeType": "JUNCTION",
          "elevationM": 12.2,
          "maxDepthM": 0.35,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.4,
          "pondedAreaM2": 18.0,
          "map": {
            "x": 1985.0,
            "y": 1654.0
          }
        },
        {
          "id": "sep_catch_basin_2",
          "nodeType": "STORAGE",
          "elevationM": 11.0,
          "maxDepthM": 1.2,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 2.0,
          "map": {
            "x": 1985.0,
            "y": 1576.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_catch_basin_2_inlet_connector",
          "linkType": "ORIFICE",
          "fromNode": "road_runoff_sep_catch_basin_2",
          "toNode": "sep_catch_basin_2",
          "orificeType": "BOTTOM",
          "offsetM": 0.0,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "RECT_CLOSED",
            "geom1": 0.6,
            "geom2": 0.6,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        }
      ]
    },
    {
      "htmlId": "sep_storm_lateral_catch_basin_1",
      "label": "분류식 빗물받이 1 우수연결관",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "sep_catch_basin_1",
        "sep_storm_lateral_catch_basin_1_start",
        "sep_storm_lateral_catch_basin_1_elbow_connector",
        "sep_storm_main_1_catch_basin_1_connector"
      ],
      "swmmLinks": [
        "sep_catch_basin_1_outlet_connector",
        "sep_storm_lateral_catch_basin_1_horizontal",
        "sep_storm_lateral_catch_basin_1_vertical"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_catch_basin_1",
          "nodeType": "STORAGE",
          "elevationM": 11.0,
          "maxDepthM": 1.2,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 2.0,
          "map": {
            "x": 1195.0,
            "y": 1576.0
          }
        },
        {
          "id": "sep_storm_lateral_catch_basin_1_start",
          "nodeType": "JUNCTION",
          "elevationM": 11.33,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 1250.0,
            "y": 1586.0
          }
        },
        {
          "id": "sep_storm_lateral_catch_basin_1_elbow_connector",
          "nodeType": "JUNCTION",
          "elevationM": 11.31,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 1370.0,
            "y": 1586.0
          }
        },
        {
          "id": "sep_storm_main_1_catch_basin_1_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.75,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 30.0,
          "map": {
            "x": 1370.0,
            "y": 1370.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_catch_basin_1_outlet_connector",
          "linkType": "ORIFICE",
          "fromNode": "sep_catch_basin_1",
          "toNode": "sep_storm_lateral_catch_basin_1_start",
          "orificeType": "SIDE",
          "offsetM": 0.33,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        },
        {
          "id": "sep_storm_lateral_catch_basin_1_horizontal",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_lateral_catch_basin_1_start",
          "toNode": "sep_storm_lateral_catch_basin_1_elbow_connector",
          "lengthM": 18.0,
          "roughnessN": 0.018,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001111
        },
        {
          "id": "sep_storm_lateral_catch_basin_1_vertical",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_lateral_catch_basin_1_elbow_connector",
          "toNode": "sep_storm_main_1_catch_basin_1_connector",
          "lengthM": 30.0,
          "roughnessN": 0.018,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.2,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.085333
        }
      ]
    },
    {
      "htmlId": "sep_storm_lateral_catch_basin_2",
      "label": "분류식 빗물받이 2 우수연결관",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "sep_catch_basin_2",
        "sep_storm_lateral_catch_basin_2_start",
        "sep_storm_lateral_catch_basin_2_elbow_connector",
        "sep_storm_main_2_catch_basin_2_connector"
      ],
      "swmmLinks": [
        "sep_catch_basin_2_outlet_connector",
        "sep_storm_lateral_catch_basin_2_horizontal",
        "sep_storm_lateral_catch_basin_2_vertical"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_catch_basin_2",
          "nodeType": "STORAGE",
          "elevationM": 11.0,
          "maxDepthM": 1.2,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 2.0,
          "map": {
            "x": 1985.0,
            "y": 1576.0
          }
        },
        {
          "id": "sep_storm_lateral_catch_basin_2_start",
          "nodeType": "JUNCTION",
          "elevationM": 11.33,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2040.0,
            "y": 1586.0
          }
        },
        {
          "id": "sep_storm_lateral_catch_basin_2_elbow_connector",
          "nodeType": "JUNCTION",
          "elevationM": 11.31,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2160.0,
            "y": 1586.0
          }
        },
        {
          "id": "sep_storm_main_2_catch_basin_2_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.38,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 30.0,
          "map": {
            "x": 2160.0,
            "y": 1370.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_catch_basin_2_outlet_connector",
          "linkType": "ORIFICE",
          "fromNode": "sep_catch_basin_2",
          "toNode": "sep_storm_lateral_catch_basin_2_start",
          "orificeType": "SIDE",
          "offsetM": 0.33,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        },
        {
          "id": "sep_storm_lateral_catch_basin_2_horizontal",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_lateral_catch_basin_2_start",
          "toNode": "sep_storm_lateral_catch_basin_2_elbow_connector",
          "lengthM": 18.0,
          "roughnessN": 0.018,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001111
        },
        {
          "id": "sep_storm_lateral_catch_basin_2_vertical",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_lateral_catch_basin_2_elbow_connector",
          "toNode": "sep_storm_main_2_catch_basin_2_connector",
          "lengthM": 30.0,
          "roughnessN": 0.018,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.2,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.097667
        }
      ]
    },
    {
      "htmlId": "sep_storm_main_1",
      "label": "우수 본관 1",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "offscreen_catch_basin_storm_main_1",
        "sep_storm_main_1_catch_basin_1_connector",
        "sep_storm_manhole"
      ],
      "swmmLinks": [
        "sep_storm_main_1_upstream_segment",
        "sep_storm_main_1_downstream_segment"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "offscreen_catch_basin_storm_main_1",
          "nodeType": "JUNCTION",
          "elevationM": 8.95,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 0.0,
            "y": 1370.0
          }
        },
        {
          "id": "sep_storm_main_1_catch_basin_1_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.75,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 30.0,
          "map": {
            "x": 1370.0,
            "y": 1370.0
          }
        },
        {
          "id": "sep_storm_manhole",
          "nodeType": "JUNCTION",
          "elevationM": 8.65,
          "maxDepthM": 3.55,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 50.0,
          "map": {
            "x": 1704.0,
            "y": 1370.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_storm_main_1_upstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "offscreen_catch_basin_storm_main_1",
          "toNode": "sep_storm_main_1_catch_basin_1_connector",
          "lengthM": 175.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.2,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001143
        },
        {
          "id": "sep_storm_main_1_downstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_main_1_catch_basin_1_connector",
          "toNode": "sep_storm_manhole",
          "lengthM": 85.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.2,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001176
        }
      ]
    },
    {
      "htmlId": "sep_storm_manhole",
      "label": "분류식 우수 맨홀",
      "objectType": "manhole",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "sep_storm_manhole"
      ],
      "swmmLinks": [],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_storm_manhole",
          "nodeType": "JUNCTION",
          "elevationM": 8.65,
          "maxDepthM": 3.55,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 50.0,
          "map": {
            "x": 1704.0,
            "y": 1370.0
          }
        }
      ],
      "resolvedLinks": []
    },
    {
      "htmlId": "sep_storm_main_2",
      "label": "우수 본관 2",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "sep_storm_manhole",
        "sep_storm_main_2_catch_basin_2_connector",
        "sep_storm_main_2_outlet_connector"
      ],
      "swmmLinks": [
        "sep_storm_main_2_upstream_segment",
        "sep_storm_main_2_downstream_segment"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_storm_manhole",
          "nodeType": "JUNCTION",
          "elevationM": 8.65,
          "maxDepthM": 3.55,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 50.0,
          "map": {
            "x": 1704.0,
            "y": 1370.0
          }
        },
        {
          "id": "sep_storm_main_2_catch_basin_2_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.38,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 30.0,
          "map": {
            "x": 2160.0,
            "y": 1370.0
          }
        },
        {
          "id": "sep_storm_main_2_outlet_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.32,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 50.0,
          "map": {
            "x": 2240.0,
            "y": 1370.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_storm_main_2_upstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_manhole",
          "toNode": "sep_storm_main_2_catch_basin_2_connector",
          "lengthM": 233.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.2,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001159
        },
        {
          "id": "sep_storm_main_2_downstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_main_2_catch_basin_2_connector",
          "toNode": "sep_storm_main_2_outlet_connector",
          "lengthM": 47.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.2,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001277
        }
      ]
    },
    {
      "htmlId": "sep_storm_main_to_trunk",
      "label": "우수 본관 2에서 우수 간선관거로 내려가는 연결관",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "sep_storm_main_2_outlet_connector",
        "sep_storm_main_to_trunk_elbow_connector",
        "sep_storm_trunk_main_2_drop_connector"
      ],
      "swmmLinks": [
        "sep_storm_main_to_trunk_horizontal",
        "sep_storm_main_to_trunk_vertical"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_storm_main_2_outlet_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.32,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 50.0,
          "map": {
            "x": 2240.0,
            "y": 1370.0
          }
        },
        {
          "id": "sep_storm_main_to_trunk_elbow_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.29,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 50.0,
          "map": {
            "x": 2355.0,
            "y": 1370.0
          }
        },
        {
          "id": "sep_storm_trunk_main_2_drop_connector",
          "nodeType": "JUNCTION",
          "elevationM": 5.6,
          "maxDepthM": 3.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2355.0,
            "y": 766.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_storm_main_to_trunk_horizontal",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_main_2_outlet_connector",
          "toNode": "sep_storm_main_to_trunk_elbow_connector",
          "lengthM": 24.0,
          "roughnessN": 0.016,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.00125
        },
        {
          "id": "sep_storm_main_to_trunk_vertical",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_main_to_trunk_elbow_connector",
          "toNode": "sep_storm_trunk_main_2_drop_connector",
          "lengthM": 40.0,
          "roughnessN": 0.016,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.5,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.06725
        }
      ]
    },
    {
      "htmlId": "sep_storm_trunk",
      "label": "우수 간선관거",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "sep_storm_trunk_upstream",
        "sep_storm_trunk_main_2_drop_connector",
        "sep_storm_trunk_downstream",
        "storm_pump_inlet_gate_node"
      ],
      "swmmLinks": [
        "sep_storm_trunk_upstream_segment",
        "sep_storm_trunk_downstream_segment",
        "sep_storm_trunk_to_pump_station"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_storm_trunk_upstream",
          "nodeType": "JUNCTION",
          "elevationM": 6.16,
          "maxDepthM": 3.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 0.0,
            "y": 766.0
          }
        },
        {
          "id": "sep_storm_trunk_main_2_drop_connector",
          "nodeType": "JUNCTION",
          "elevationM": 5.6,
          "maxDepthM": 3.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2355.0,
            "y": 766.0
          }
        },
        {
          "id": "sep_storm_trunk_downstream",
          "nodeType": "JUNCTION",
          "elevationM": 5.01,
          "maxDepthM": 3.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 4800.0,
            "y": 766.0
          }
        },
        {
          "id": "storm_pump_inlet_gate_node",
          "nodeType": "JUNCTION",
          "elevationM": 4.95,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 4885.0,
            "y": 762.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_storm_trunk_upstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_trunk_upstream",
          "toNode": "sep_storm_trunk_main_2_drop_connector",
          "lengthM": 490.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001143
        },
        {
          "id": "sep_storm_trunk_downstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_trunk_main_2_drop_connector",
          "toNode": "sep_storm_trunk_downstream",
          "lengthM": 510.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001157
        },
        {
          "id": "sep_storm_trunk_to_pump_station",
          "linkType": "CONDUIT",
          "fromNode": "sep_storm_trunk_downstream",
          "toNode": "storm_pump_inlet_gate_node",
          "lengthM": 35.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001714
        }
      ]
    },
    {
      "htmlId": "storm_pump_station",
      "label": "빗물펌프장",
      "objectType": "pump_station",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "storm_pump_inlet_gate_node",
        "storm_pump_station",
        "storm_pump_discharge_node"
      ],
      "swmmLinks": [
        "storm_pump_inlet_gate",
        "storm_pump_unit"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true,
        "operation": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "storm_pump_inlet_gate_node",
          "nodeType": "JUNCTION",
          "elevationM": 4.95,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 4885.0,
            "y": 762.0
          }
        },
        {
          "id": "storm_pump_station",
          "nodeType": "STORAGE",
          "elevationM": 4.7,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 25.0,
          "map": {
            "x": 5092.0,
            "y": 762.0
          }
        },
        {
          "id": "storm_pump_discharge_node",
          "nodeType": "JUNCTION",
          "elevationM": 5.2,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5400.0,
            "y": 761.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "storm_pump_inlet_gate",
          "linkType": "ORIFICE",
          "fromNode": "storm_pump_inlet_gate_node",
          "toNode": "storm_pump_station",
          "orificeType": "SIDE",
          "offsetM": 0.0,
          "qCoeff": 0.75,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        },
        {
          "id": "storm_pump_unit",
          "linkType": "PUMP",
          "fromNode": "storm_pump_station",
          "toNode": "storm_pump_discharge_node",
          "pumpCurve": "STORM_PUMP_CURVE",
          "initialStatus": "OFF",
          "startupDepthM": 0.8,
          "shutoffDepthM": 0.25
        }
      ]
    },
    {
      "htmlId": "storm_pump_discharge_pipe",
      "label": "펌프 토출관",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "storm_pump_discharge_node",
        "pump_outfall_gate_node"
      ],
      "swmmLinks": [
        "storm_pump_discharge_pipe"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "storm_pump_discharge_node",
          "nodeType": "JUNCTION",
          "elevationM": 5.2,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5400.0,
            "y": 761.0
          }
        },
        {
          "id": "pump_outfall_gate_node",
          "nodeType": "JUNCTION",
          "elevationM": 5.03,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5870.0,
            "y": 761.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "storm_pump_discharge_pipe",
          "linkType": "CONDUIT",
          "fromNode": "storm_pump_discharge_node",
          "toNode": "pump_outfall_gate_node",
          "lengthM": 145.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001172
        }
      ]
    },
    {
      "htmlId": "pump_outfall",
      "label": "펌프 방류구",
      "objectType": "outfall",
      "system": "separate",
      "waterType": "storm",
      "swmmNodes": [
        "pump_outfall_gate_node",
        "pump_outfall"
      ],
      "swmmLinks": [
        "pump_outfall_gate"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "pump_outfall_gate_node",
          "nodeType": "JUNCTION",
          "elevationM": 5.03,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5870.0,
            "y": 761.0
          }
        },
        {
          "id": "pump_outfall",
          "nodeType": "OUTFALL",
          "elevationM": 5.02,
          "outfallType": "FREE",
          "gated": "NO",
          "map": {
            "x": 6054.0,
            "y": 761.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "pump_outfall_gate",
          "linkType": "ORIFICE",
          "fromNode": "pump_outfall_gate_node",
          "toNode": "pump_outfall",
          "orificeType": "SIDE",
          "offsetM": 0.0,
          "qCoeff": 0.75,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        }
      ]
    },
    {
      "htmlId": "sep_sewer_lateral_apartment_1",
      "label": "분류식 아파트 1 오수연결관",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "sewer",
      "swmmNodes": [
        "sep_apartment_1",
        "sep_sewer_lateral_apartment_1_elbow_connector",
        "sep_sewer_main_1_apartment_1_connector"
      ],
      "swmmLinks": [
        "sep_sewer_lateral_apartment_1_horizontal",
        "sep_sewer_lateral_apartment_1_vertical"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_apartment_1",
          "nodeType": "JUNCTION",
          "elevationM": 11.35,
          "maxDepthM": 1.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 245.0,
            "y": 1682.0
          }
        },
        {
          "id": "sep_sewer_lateral_apartment_1_elbow_connector",
          "nodeType": "JUNCTION",
          "elevationM": 11.33,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 365.0,
            "y": 1682.0
          }
        },
        {
          "id": "sep_sewer_main_1_apartment_1_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.55,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 365.0,
            "y": 1075.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_sewer_lateral_apartment_1_horizontal",
          "linkType": "CONDUIT",
          "fromNode": "sep_apartment_1",
          "toNode": "sep_sewer_lateral_apartment_1_elbow_connector",
          "lengthM": 18.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001111
        },
        {
          "id": "sep_sewer_lateral_apartment_1_vertical",
          "linkType": "CONDUIT",
          "fromNode": "sep_sewer_lateral_apartment_1_elbow_connector",
          "toNode": "sep_sewer_main_1_apartment_1_connector",
          "lengthM": 30.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.2,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.092667
        }
      ]
    },
    {
      "htmlId": "sep_sewer_lateral_apartment_2",
      "label": "분류식 아파트 2 오수연결관",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "sewer",
      "swmmNodes": [
        "sep_apartment_2",
        "sep_sewer_lateral_apartment_2_elbow_connector",
        "sep_sewer_main_2_apartment_2_connector"
      ],
      "swmmLinks": [
        "sep_sewer_lateral_apartment_2_horizontal",
        "sep_sewer_lateral_apartment_2_vertical"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_apartment_2",
          "nodeType": "JUNCTION",
          "elevationM": 11.3,
          "maxDepthM": 1.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 847.0,
            "y": 1682.0
          }
        },
        {
          "id": "sep_sewer_lateral_apartment_2_elbow_connector",
          "nodeType": "JUNCTION",
          "elevationM": 11.28,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 727.0,
            "y": 1682.0
          }
        },
        {
          "id": "sep_sewer_main_2_apartment_2_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.35,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 727.0,
            "y": 1075.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_sewer_lateral_apartment_2_horizontal",
          "linkType": "CONDUIT",
          "fromNode": "sep_apartment_2",
          "toNode": "sep_sewer_lateral_apartment_2_elbow_connector",
          "lengthM": 18.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001111
        },
        {
          "id": "sep_sewer_lateral_apartment_2_vertical",
          "linkType": "CONDUIT",
          "fromNode": "sep_sewer_lateral_apartment_2_elbow_connector",
          "toNode": "sep_sewer_main_2_apartment_2_connector",
          "lengthM": 30.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.2,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.097667
        }
      ]
    },
    {
      "htmlId": "sep_sewer_main_1",
      "label": "오수 본관 1",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "sewer",
      "swmmNodes": [
        "sep_sewer_upstream",
        "sep_sewer_main_1_apartment_1_connector",
        "sep_sewer_manhole"
      ],
      "swmmLinks": [
        "sep_sewer_main_1_upstream_segment",
        "sep_sewer_main_1_downstream_segment"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_sewer_upstream",
          "nodeType": "JUNCTION",
          "elevationM": 8.7,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 0.0,
            "y": 1075.0
          }
        },
        {
          "id": "sep_sewer_main_1_apartment_1_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.55,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 365.0,
            "y": 1075.0
          }
        },
        {
          "id": "sep_sewer_manhole",
          "nodeType": "JUNCTION",
          "elevationM": 8.45,
          "maxDepthM": 3.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 1.2,
          "pondedAreaM2": 20.0,
          "map": {
            "x": 546.0,
            "y": 1075.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_sewer_main_1_upstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "sep_sewer_upstream",
          "toNode": "sep_sewer_main_1_apartment_1_connector",
          "lengthM": 185.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.05,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.000811
        },
        {
          "id": "sep_sewer_main_1_downstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "sep_sewer_main_1_apartment_1_connector",
          "toNode": "sep_sewer_manhole",
          "lengthM": 45.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.05,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.002222
        }
      ]
    },
    {
      "htmlId": "sep_sewer_manhole",
      "label": "분류식 오수 맨홀",
      "objectType": "manhole",
      "system": "separate",
      "waterType": "sewer",
      "swmmNodes": [
        "sep_sewer_manhole"
      ],
      "swmmLinks": [],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_sewer_manhole",
          "nodeType": "JUNCTION",
          "elevationM": 8.45,
          "maxDepthM": 3.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 1.2,
          "pondedAreaM2": 20.0,
          "map": {
            "x": 546.0,
            "y": 1075.0
          }
        }
      ],
      "resolvedLinks": []
    },
    {
      "htmlId": "sep_sewer_main_2",
      "label": "오수 본관 2",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "sewer",
      "swmmNodes": [
        "sep_sewer_manhole",
        "sep_sewer_main_2_apartment_2_connector",
        "sep_sewer_downstream"
      ],
      "swmmLinks": [
        "sep_sewer_main_2_upstream_segment",
        "sep_sewer_main_2_downstream_segment"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_sewer_manhole",
          "nodeType": "JUNCTION",
          "elevationM": 8.45,
          "maxDepthM": 3.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 1.2,
          "pondedAreaM2": 20.0,
          "map": {
            "x": 546.0,
            "y": 1075.0
          }
        },
        {
          "id": "sep_sewer_main_2_apartment_2_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.35,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 727.0,
            "y": 1075.0
          }
        },
        {
          "id": "sep_sewer_downstream",
          "nodeType": "JUNCTION",
          "elevationM": 8.1,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2170.0,
            "y": 1075.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_sewer_main_2_upstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "sep_sewer_manhole",
          "toNode": "sep_sewer_main_2_apartment_2_connector",
          "lengthM": 60.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.05,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001667
        },
        {
          "id": "sep_sewer_main_2_downstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "sep_sewer_main_2_apartment_2_connector",
          "toNode": "sep_sewer_downstream",
          "lengthM": 200.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.05,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.00125
        }
      ]
    },
    {
      "htmlId": "sep_sewer_main_to_interceptor",
      "label": "오수 본관 2에서 차집관거로 내려가는 연결관",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "sewer",
      "swmmNodes": [
        "sep_sewer_downstream",
        "sep_sewer_main_to_interceptor_elbow_connector",
        "sep_interceptor_join"
      ],
      "swmmLinks": [
        "sep_sewer_main_to_interceptor_horizontal",
        "sep_sewer_main_to_interceptor_vertical"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_sewer_downstream",
          "nodeType": "JUNCTION",
          "elevationM": 8.1,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2170.0,
            "y": 1075.0
          }
        },
        {
          "id": "sep_sewer_main_to_interceptor_elbow_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.07,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2264.0,
            "y": 1075.0
          }
        },
        {
          "id": "sep_interceptor_join",
          "nodeType": "JUNCTION",
          "elevationM": 6.2,
          "maxDepthM": 3.2,
          "initialDepthM": 0.0,
          "surchargeDepthM": 1.0,
          "pondedAreaM2": 20.0,
          "map": {
            "x": 2264.0,
            "y": 231.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_sewer_main_to_interceptor_horizontal",
          "linkType": "CONDUIT",
          "fromNode": "sep_sewer_downstream",
          "toNode": "sep_sewer_main_to_interceptor_elbow_connector",
          "lengthM": 24.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.05,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.00125
        },
        {
          "id": "sep_sewer_main_to_interceptor_vertical",
          "linkType": "CONDUIT",
          "fromNode": "sep_sewer_main_to_interceptor_elbow_connector",
          "toNode": "sep_interceptor_join",
          "lengthM": 40.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.05,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.5,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.04675
        }
      ]
    },
    {
      "htmlId": "sep_interceptor",
      "label": "차집관거",
      "objectType": "pipe_group",
      "system": "separate",
      "waterType": "sewer",
      "swmmNodes": [
        "sep_interceptor_upstream",
        "sep_interceptor_join",
        "overflow_interceptor_join",
        "sep_interceptor_downstream",
        "water_reclamation_center"
      ],
      "swmmLinks": [
        "sep_interceptor_upstream_segment",
        "sep_interceptor_join_to_overflow_segment",
        "sep_interceptor_downstream_segment",
        "sep_interceptor_to_reclamation_inlet"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "sep_interceptor_upstream",
          "nodeType": "JUNCTION",
          "elevationM": 6.55,
          "maxDepthM": 3.2,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.8,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 0.0,
            "y": 231.0
          }
        },
        {
          "id": "sep_interceptor_join",
          "nodeType": "JUNCTION",
          "elevationM": 6.2,
          "maxDepthM": 3.2,
          "initialDepthM": 0.0,
          "surchargeDepthM": 1.0,
          "pondedAreaM2": 20.0,
          "map": {
            "x": 2264.0,
            "y": 231.0
          }
        },
        {
          "id": "overflow_interceptor_join",
          "nodeType": "JUNCTION",
          "elevationM": 5.65,
          "maxDepthM": 3.2,
          "initialDepthM": 0.0,
          "surchargeDepthM": 1.0,
          "pondedAreaM2": 20.0,
          "map": {
            "x": 4753.0,
            "y": 231.0
          }
        },
        {
          "id": "sep_interceptor_downstream",
          "nodeType": "JUNCTION",
          "elevationM": 5.6,
          "maxDepthM": 3.2,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.8,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 4978.0,
            "y": 231.0
          }
        },
        {
          "id": "water_reclamation_center",
          "nodeType": "STORAGE",
          "elevationM": 5.05,
          "maxDepthM": 4.0,
          "initialDepthM": 0.15,
          "shape": "FUNCTIONAL",
          "storageParam": 120.0,
          "map": {
            "x": 5270.0,
            "y": 228.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "sep_interceptor_upstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "sep_interceptor_upstream",
          "toNode": "sep_interceptor_join",
          "lengthM": 460.0,
          "roughnessN": 0.016,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.000761
        },
        {
          "id": "sep_interceptor_join_to_overflow_segment",
          "linkType": "CONDUIT",
          "fromNode": "sep_interceptor_join",
          "toNode": "overflow_interceptor_join",
          "lengthM": 570.0,
          "roughnessN": 0.016,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.000965
        },
        {
          "id": "sep_interceptor_downstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "overflow_interceptor_join",
          "toNode": "sep_interceptor_downstream",
          "lengthM": 50.0,
          "roughnessN": 0.016,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001
        },
        {
          "id": "sep_interceptor_to_reclamation_inlet",
          "linkType": "CONDUIT",
          "fromNode": "sep_interceptor_downstream",
          "toNode": "water_reclamation_center",
          "lengthM": 45.0,
          "roughnessN": 0.016,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.012222
        }
      ]
    },
    {
      "htmlId": "water_reclamation_center",
      "label": "물재생센터",
      "objectType": "treatment_facility",
      "system": "treatment",
      "waterType": "treated",
      "swmmNodes": [
        "water_reclamation_center",
        "treatment_process_outlet_node"
      ],
      "swmmLinks": [
        "treatment_process_limited_outlet"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true,
        "operation": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "water_reclamation_center",
          "nodeType": "STORAGE",
          "elevationM": 5.05,
          "maxDepthM": 4.0,
          "initialDepthM": 0.15,
          "shape": "FUNCTIONAL",
          "storageParam": 120.0,
          "map": {
            "x": 5270.0,
            "y": 228.0
          }
        },
        {
          "id": "treatment_process_outlet_node",
          "nodeType": "JUNCTION",
          "elevationM": 4.95,
          "maxDepthM": 3.2,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.8,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5578.0,
            "y": 223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "treatment_process_limited_outlet",
          "linkType": "CONDUIT",
          "fromNode": "water_reclamation_center",
          "toNode": "treatment_process_outlet_node",
          "lengthM": 30.0,
          "roughnessN": 0.014,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.02,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.2,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.003333
        }
      ]
    },
    {
      "htmlId": "treatment_effluent_pipe",
      "label": "처리수 방류관",
      "objectType": "pipe_group",
      "system": "treatment",
      "waterType": "treated",
      "swmmNodes": [
        "treatment_process_outlet_node",
        "treated_outfall_gate_node"
      ],
      "swmmLinks": [
        "treatment_effluent_pipe"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "treatment_process_outlet_node",
          "nodeType": "JUNCTION",
          "elevationM": 4.95,
          "maxDepthM": 3.2,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.8,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5578.0,
            "y": 223.0
          }
        },
        {
          "id": "treated_outfall_gate_node",
          "nodeType": "JUNCTION",
          "elevationM": 4.86,
          "maxDepthM": 3.2,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.8,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5870.0,
            "y": 223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "treatment_effluent_pipe",
          "linkType": "CONDUIT",
          "fromNode": "treatment_process_outlet_node",
          "toNode": "treated_outfall_gate_node",
          "lengthM": 300.0,
          "roughnessN": 0.014,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.0003
        }
      ]
    },
    {
      "htmlId": "treated_outfall",
      "label": "처리수 방류구",
      "objectType": "outfall",
      "system": "treatment",
      "waterType": "treated",
      "swmmNodes": [
        "treated_outfall_gate_node",
        "treated_outfall"
      ],
      "swmmLinks": [
        "treated_outfall_gate"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "treated_outfall_gate_node",
          "nodeType": "JUNCTION",
          "elevationM": 4.86,
          "maxDepthM": 3.2,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.8,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5870.0,
            "y": 223.0
          }
        },
        {
          "id": "treated_outfall",
          "nodeType": "OUTFALL",
          "elevationM": 4.85,
          "outfallType": "FREE",
          "gated": "NO",
          "map": {
            "x": 6028.0,
            "y": 223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "treated_outfall_gate",
          "linkType": "ORIFICE",
          "fromNode": "treated_outfall_gate_node",
          "toNode": "treated_outfall",
          "orificeType": "SIDE",
          "offsetM": 0.0,
          "qCoeff": 0.75,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        }
      ]
    },
    {
      "htmlId": "comb_house_1",
      "label": "합류식 주거지 1",
      "objectType": "surface",
      "system": "combined",
      "waterType": "sewer",
      "swmmNodes": [
        "comb_house_1"
      ],
      "swmmLinks": [],
      "controls": {
        "rainfall": false,
        "blockage": false
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "comb_house_1",
          "nodeType": "JUNCTION",
          "elevationM": 11.1,
          "maxDepthM": 1.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2645.0,
            "y": 1682.0
          }
        }
      ],
      "resolvedLinks": []
    },
    {
      "htmlId": "comb_house_2",
      "label": "합류식 주거지 2",
      "objectType": "surface",
      "system": "combined",
      "waterType": "sewer",
      "swmmNodes": [
        "comb_house_2"
      ],
      "swmmLinks": [],
      "controls": {
        "rainfall": false,
        "blockage": false
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "comb_house_2",
          "nodeType": "JUNCTION",
          "elevationM": 11.0,
          "maxDepthM": 1.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 3075.0,
            "y": 1682.0
          }
        }
      ],
      "resolvedLinks": []
    },
    {
      "htmlId": "offscreen_comb_catch_basin",
      "label": "합류식 화면밖 빗물받이",
      "objectType": "catch_basin",
      "system": "combined",
      "waterType": "storm",
      "swmmNodes": [
        "road_runoff_offscreen_comb_catch_basin",
        "offscreen_comb_catch_basin"
      ],
      "swmmLinks": [
        "offscreen_comb_catch_basin_inlet_connector"
      ],
      "controls": {
        "rainfall": true,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "road_runoff_offscreen_comb_catch_basin",
          "nodeType": "JUNCTION",
          "elevationM": 12.2,
          "maxDepthM": 0.35,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.4,
          "pondedAreaM2": 18.0,
          "map": {
            "x": 2440.0,
            "y": 1654.0
          }
        },
        {
          "id": "offscreen_comb_catch_basin",
          "nodeType": "STORAGE",
          "elevationM": 11.0,
          "maxDepthM": 1.2,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 2.0,
          "map": {
            "x": 2440.0,
            "y": 1576.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "offscreen_comb_catch_basin_inlet_connector",
          "linkType": "ORIFICE",
          "fromNode": "road_runoff_offscreen_comb_catch_basin",
          "toNode": "offscreen_comb_catch_basin",
          "orificeType": "BOTTOM",
          "offsetM": 0.0,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "RECT_CLOSED",
            "geom1": 0.6,
            "geom2": 0.6,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        }
      ]
    },
    {
      "htmlId": "comb_catch_basin_1",
      "label": "합류식 빗물받이 1",
      "objectType": "catch_basin",
      "system": "combined",
      "waterType": "storm",
      "swmmNodes": [
        "road_runoff_comb_catch_basin_1",
        "comb_catch_basin_1"
      ],
      "swmmLinks": [
        "comb_catch_basin_1_inlet_connector"
      ],
      "controls": {
        "rainfall": true,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "road_runoff_comb_catch_basin_1",
          "nodeType": "JUNCTION",
          "elevationM": 12.2,
          "maxDepthM": 0.35,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.4,
          "pondedAreaM2": 18.0,
          "map": {
            "x": 3475.0,
            "y": 1654.0
          }
        },
        {
          "id": "comb_catch_basin_1",
          "nodeType": "STORAGE",
          "elevationM": 11.0,
          "maxDepthM": 1.2,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 2.0,
          "map": {
            "x": 3475.0,
            "y": 1576.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "comb_catch_basin_1_inlet_connector",
          "linkType": "ORIFICE",
          "fromNode": "road_runoff_comb_catch_basin_1",
          "toNode": "comb_catch_basin_1",
          "orificeType": "BOTTOM",
          "offsetM": 0.0,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "RECT_CLOSED",
            "geom1": 0.6,
            "geom2": 0.6,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        }
      ]
    },
    {
      "htmlId": "comb_catch_basin_2",
      "label": "합류식 빗물받이 2",
      "objectType": "catch_basin",
      "system": "combined",
      "waterType": "storm",
      "swmmNodes": [
        "road_runoff_comb_catch_basin_2",
        "comb_catch_basin_2"
      ],
      "swmmLinks": [
        "comb_catch_basin_2_inlet_connector"
      ],
      "controls": {
        "rainfall": true,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "road_runoff_comb_catch_basin_2",
          "nodeType": "JUNCTION",
          "elevationM": 12.2,
          "maxDepthM": 0.35,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.4,
          "pondedAreaM2": 18.0,
          "map": {
            "x": 4225.0,
            "y": 1654.0
          }
        },
        {
          "id": "comb_catch_basin_2",
          "nodeType": "STORAGE",
          "elevationM": 10.95,
          "maxDepthM": 1.2,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 2.0,
          "map": {
            "x": 4225.0,
            "y": 1576.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "comb_catch_basin_2_inlet_connector",
          "linkType": "ORIFICE",
          "fromNode": "road_runoff_comb_catch_basin_2",
          "toNode": "comb_catch_basin_2",
          "orificeType": "BOTTOM",
          "offsetM": 0.0,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "RECT_CLOSED",
            "geom1": 0.6,
            "geom2": 0.6,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        }
      ]
    },
    {
      "htmlId": "offscreen_comb_storm_lateral",
      "label": "합류식 화면밖 우수연결관",
      "objectType": "pipe_group",
      "system": "combined",
      "waterType": "storm",
      "swmmNodes": [
        "offscreen_comb_catch_basin",
        "offscreen_comb_storm_lateral_start",
        "offscreen_comb_storm_lateral_elbow_connector",
        "comb_upstream"
      ],
      "swmmLinks": [
        "offscreen_comb_catch_basin_outlet_connector",
        "offscreen_comb_storm_lateral_horizontal",
        "offscreen_comb_storm_lateral_vertical"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "offscreen_comb_catch_basin",
          "nodeType": "STORAGE",
          "elevationM": 11.0,
          "maxDepthM": 1.2,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 2.0,
          "map": {
            "x": 2440.0,
            "y": 1576.0
          }
        },
        {
          "id": "offscreen_comb_storm_lateral_start",
          "nodeType": "JUNCTION",
          "elevationM": 11.33,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2480.0,
            "y": 1586.0
          }
        },
        {
          "id": "offscreen_comb_storm_lateral_elbow_connector",
          "nodeType": "JUNCTION",
          "elevationM": 11.31,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2510.0,
            "y": 1586.0
          }
        },
        {
          "id": "comb_upstream",
          "nodeType": "JUNCTION",
          "elevationM": 8.82,
          "maxDepthM": 2.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2440.0,
            "y": 1223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "offscreen_comb_catch_basin_outlet_connector",
          "linkType": "ORIFICE",
          "fromNode": "offscreen_comb_catch_basin",
          "toNode": "offscreen_comb_storm_lateral_start",
          "orificeType": "SIDE",
          "offsetM": 0.33,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        },
        {
          "id": "offscreen_comb_storm_lateral_horizontal",
          "linkType": "CONDUIT",
          "fromNode": "offscreen_comb_storm_lateral_start",
          "toNode": "offscreen_comb_storm_lateral_elbow_connector",
          "lengthM": 18.0,
          "roughnessN": 0.018,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001111
        },
        {
          "id": "offscreen_comb_storm_lateral_vertical",
          "linkType": "CONDUIT",
          "fromNode": "offscreen_comb_storm_lateral_elbow_connector",
          "toNode": "comb_upstream",
          "lengthM": 30.0,
          "roughnessN": 0.018,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.2,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.083
        }
      ]
    },
    {
      "htmlId": "offscreen_comb_sewer_lateral",
      "label": "합류식 화면밖 오수연결관",
      "objectType": "pipe_group",
      "system": "combined",
      "waterType": "sewer",
      "swmmNodes": [
        "offscreen_comb_sewer_source",
        "comb_upstream"
      ],
      "swmmLinks": [
        "offscreen_comb_sewer_lateral"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "offscreen_comb_sewer_source",
          "nodeType": "JUNCTION",
          "elevationM": 8.88,
          "maxDepthM": 1.2,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.4,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2440.0,
            "y": 1262.0
          }
        },
        {
          "id": "comb_upstream",
          "nodeType": "JUNCTION",
          "elevationM": 8.82,
          "maxDepthM": 2.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2440.0,
            "y": 1223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "offscreen_comb_sewer_lateral",
          "linkType": "CONDUIT",
          "fromNode": "offscreen_comb_sewer_source",
          "toNode": "comb_upstream",
          "lengthM": 24.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.0025
        }
      ]
    },
    {
      "htmlId": "comb_sewer_lateral_house_1",
      "label": "합류식 주거지 1 오수연결관",
      "objectType": "pipe_group",
      "system": "combined",
      "waterType": "sewer",
      "swmmNodes": [
        "comb_house_1",
        "comb_sewer_lateral_house_1_elbow_connector",
        "comb_main_house_1_connector"
      ],
      "swmmLinks": [
        "comb_sewer_lateral_house_1_horizontal",
        "comb_sewer_lateral_house_1_vertical"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "comb_house_1",
          "nodeType": "JUNCTION",
          "elevationM": 11.1,
          "maxDepthM": 1.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2645.0,
            "y": 1682.0
          }
        },
        {
          "id": "comb_sewer_lateral_house_1_elbow_connector",
          "nodeType": "JUNCTION",
          "elevationM": 11.08,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2850.0,
            "y": 1682.0
          }
        },
        {
          "id": "comb_main_house_1_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.6,
          "maxDepthM": 2.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2850.0,
            "y": 1223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "comb_sewer_lateral_house_1_horizontal",
          "linkType": "CONDUIT",
          "fromNode": "comb_house_1",
          "toNode": "comb_sewer_lateral_house_1_elbow_connector",
          "lengthM": 18.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001111
        },
        {
          "id": "comb_sewer_lateral_house_1_vertical",
          "linkType": "CONDUIT",
          "fromNode": "comb_sewer_lateral_house_1_elbow_connector",
          "toNode": "comb_main_house_1_connector",
          "lengthM": 30.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.2,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.082667
        }
      ]
    },
    {
      "htmlId": "comb_sewer_lateral_house_2",
      "label": "합류식 주거지 2 오수연결관",
      "objectType": "pipe_group",
      "system": "combined",
      "waterType": "sewer",
      "swmmNodes": [
        "comb_house_2",
        "comb_sewer_lateral_house_2_elbow_connector",
        "comb_main_house_2_connector"
      ],
      "swmmLinks": [
        "comb_sewer_lateral_house_2_horizontal",
        "comb_sewer_lateral_house_2_vertical"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "comb_house_2",
          "nodeType": "JUNCTION",
          "elevationM": 11.0,
          "maxDepthM": 1.0,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 3075.0,
            "y": 1682.0
          }
        },
        {
          "id": "comb_sewer_lateral_house_2_elbow_connector",
          "nodeType": "JUNCTION",
          "elevationM": 10.98,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 3280.0,
            "y": 1682.0
          }
        },
        {
          "id": "comb_main_house_2_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.54,
          "maxDepthM": 2.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 3280.0,
            "y": 1223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "comb_sewer_lateral_house_2_horizontal",
          "linkType": "CONDUIT",
          "fromNode": "comb_house_2",
          "toNode": "comb_sewer_lateral_house_2_elbow_connector",
          "lengthM": 18.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001111
        },
        {
          "id": "comb_sewer_lateral_house_2_vertical",
          "linkType": "CONDUIT",
          "fromNode": "comb_sewer_lateral_house_2_elbow_connector",
          "toNode": "comb_main_house_2_connector",
          "lengthM": 30.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.2,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.081333
        }
      ]
    },
    {
      "htmlId": "comb_storm_lateral_catch_basin_1",
      "label": "합류식 빗물받이 1 우수연결관",
      "objectType": "pipe_group",
      "system": "combined",
      "waterType": "storm",
      "swmmNodes": [
        "comb_catch_basin_1",
        "comb_storm_lateral_catch_basin_1_start",
        "comb_storm_lateral_catch_basin_1_elbow_connector",
        "comb_main_catch_basin_1_connector"
      ],
      "swmmLinks": [
        "comb_catch_basin_1_outlet_connector",
        "comb_storm_lateral_catch_basin_1_horizontal",
        "comb_storm_lateral_catch_basin_1_vertical"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "comb_catch_basin_1",
          "nodeType": "STORAGE",
          "elevationM": 11.0,
          "maxDepthM": 1.2,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 2.0,
          "map": {
            "x": 3475.0,
            "y": 1576.0
          }
        },
        {
          "id": "comb_storm_lateral_catch_basin_1_start",
          "nodeType": "JUNCTION",
          "elevationM": 11.33,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 3530.0,
            "y": 1586.0
          }
        },
        {
          "id": "comb_storm_lateral_catch_basin_1_elbow_connector",
          "nodeType": "JUNCTION",
          "elevationM": 11.31,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 3650.0,
            "y": 1586.0
          }
        },
        {
          "id": "comb_main_catch_basin_1_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.43,
          "maxDepthM": 2.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 3650.0,
            "y": 1223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "comb_catch_basin_1_outlet_connector",
          "linkType": "ORIFICE",
          "fromNode": "comb_catch_basin_1",
          "toNode": "comb_storm_lateral_catch_basin_1_start",
          "orificeType": "SIDE",
          "offsetM": 0.33,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        },
        {
          "id": "comb_storm_lateral_catch_basin_1_horizontal",
          "linkType": "CONDUIT",
          "fromNode": "comb_storm_lateral_catch_basin_1_start",
          "toNode": "comb_storm_lateral_catch_basin_1_elbow_connector",
          "lengthM": 18.0,
          "roughnessN": 0.018,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001111
        },
        {
          "id": "comb_storm_lateral_catch_basin_1_vertical",
          "linkType": "CONDUIT",
          "fromNode": "comb_storm_lateral_catch_basin_1_elbow_connector",
          "toNode": "comb_main_catch_basin_1_connector",
          "lengthM": 30.0,
          "roughnessN": 0.018,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.2,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.096
        }
      ]
    },
    {
      "htmlId": "comb_storm_lateral_catch_basin_2",
      "label": "합류식 빗물받이 2 우수연결관",
      "objectType": "pipe_group",
      "system": "combined",
      "waterType": "storm",
      "swmmNodes": [
        "comb_catch_basin_2",
        "comb_storm_lateral_catch_basin_2_start",
        "comb_storm_lateral_catch_basin_2_elbow_connector",
        "comb_main_catch_basin_2_connector"
      ],
      "swmmLinks": [
        "comb_catch_basin_2_outlet_connector",
        "comb_storm_lateral_catch_basin_2_horizontal",
        "comb_storm_lateral_catch_basin_2_vertical"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "comb_catch_basin_2",
          "nodeType": "STORAGE",
          "elevationM": 10.95,
          "maxDepthM": 1.2,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 2.0,
          "map": {
            "x": 4225.0,
            "y": 1576.0
          }
        },
        {
          "id": "comb_storm_lateral_catch_basin_2_start",
          "nodeType": "JUNCTION",
          "elevationM": 11.28,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 4280.0,
            "y": 1586.0
          }
        },
        {
          "id": "comb_storm_lateral_catch_basin_2_elbow_connector",
          "nodeType": "JUNCTION",
          "elevationM": 11.26,
          "maxDepthM": 0.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.3,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 4400.0,
            "y": 1586.0
          }
        },
        {
          "id": "comb_main_catch_basin_2_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.18,
          "maxDepthM": 2.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 4400.0,
            "y": 1223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "comb_catch_basin_2_outlet_connector",
          "linkType": "ORIFICE",
          "fromNode": "comb_catch_basin_2",
          "toNode": "comb_storm_lateral_catch_basin_2_start",
          "orificeType": "SIDE",
          "offsetM": 0.33,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        },
        {
          "id": "comb_storm_lateral_catch_basin_2_horizontal",
          "linkType": "CONDUIT",
          "fromNode": "comb_storm_lateral_catch_basin_2_start",
          "toNode": "comb_storm_lateral_catch_basin_2_elbow_connector",
          "lengthM": 18.0,
          "roughnessN": 0.018,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001111
        },
        {
          "id": "comb_storm_lateral_catch_basin_2_vertical",
          "linkType": "CONDUIT",
          "fromNode": "comb_storm_lateral_catch_basin_2_elbow_connector",
          "toNode": "comb_main_catch_basin_2_connector",
          "lengthM": 30.0,
          "roughnessN": 0.018,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.45,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.2,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.102667
        }
      ]
    },
    {
      "htmlId": "comb_main_1",
      "label": "합류식 본관 1",
      "objectType": "pipe_group",
      "system": "combined",
      "waterType": "combined",
      "swmmNodes": [
        "comb_upstream",
        "comb_main_house_1_connector",
        "comb_main_house_2_connector",
        "comb_main_catch_basin_1_connector",
        "combined_manhole"
      ],
      "swmmLinks": [
        "comb_main_1_upstream_segment",
        "comb_main_1_house_1_to_house_2_segment",
        "comb_main_1_house_2_to_catch_basin_1_segment",
        "comb_main_1_to_manhole_segment"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "comb_upstream",
          "nodeType": "JUNCTION",
          "elevationM": 8.82,
          "maxDepthM": 2.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2440.0,
            "y": 1223.0
          }
        },
        {
          "id": "comb_main_house_1_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.6,
          "maxDepthM": 2.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 2850.0,
            "y": 1223.0
          }
        },
        {
          "id": "comb_main_house_2_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.54,
          "maxDepthM": 2.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 3280.0,
            "y": 1223.0
          }
        },
        {
          "id": "comb_main_catch_basin_1_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.43,
          "maxDepthM": 2.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 3650.0,
            "y": 1223.0
          }
        },
        {
          "id": "combined_manhole",
          "nodeType": "JUNCTION",
          "elevationM": 8.35,
          "maxDepthM": 3.5,
          "initialDepthM": 0.0,
          "surchargeDepthM": 1.2,
          "pondedAreaM2": 20.0,
          "map": {
            "x": 3900.0,
            "y": 1223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "comb_main_1_upstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "comb_upstream",
          "toNode": "comb_main_house_1_connector",
          "lengthM": 220.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.2,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001
        },
        {
          "id": "comb_main_1_house_1_to_house_2_segment",
          "linkType": "CONDUIT",
          "fromNode": "comb_main_house_1_connector",
          "toNode": "comb_main_house_2_connector",
          "lengthM": 60.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.2,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001
        },
        {
          "id": "comb_main_1_house_2_to_catch_basin_1_segment",
          "linkType": "CONDUIT",
          "fromNode": "comb_main_house_2_connector",
          "toNode": "comb_main_catch_basin_1_connector",
          "lengthM": 110.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.2,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001
        },
        {
          "id": "comb_main_1_to_manhole_segment",
          "linkType": "CONDUIT",
          "fromNode": "comb_main_catch_basin_1_connector",
          "toNode": "combined_manhole",
          "lengthM": 80.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.2,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001
        }
      ]
    },
    {
      "htmlId": "combined_manhole",
      "label": "합류식 맨홀",
      "objectType": "manhole",
      "system": "combined",
      "waterType": "combined",
      "swmmNodes": [
        "combined_manhole"
      ],
      "swmmLinks": [],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "combined_manhole",
          "nodeType": "JUNCTION",
          "elevationM": 8.35,
          "maxDepthM": 3.5,
          "initialDepthM": 0.0,
          "surchargeDepthM": 1.2,
          "pondedAreaM2": 20.0,
          "map": {
            "x": 3900.0,
            "y": 1223.0
          }
        }
      ],
      "resolvedLinks": []
    },
    {
      "htmlId": "comb_main_2",
      "label": "합류식 본관 2",
      "objectType": "pipe_group",
      "system": "combined",
      "waterType": "combined",
      "swmmNodes": [
        "combined_manhole",
        "comb_main_catch_basin_2_connector",
        "overflow_chamber"
      ],
      "swmmLinks": [
        "comb_main_2_manhole_to_catch_basin_2_segment",
        "comb_main_2_downstream_segment"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "combined_manhole",
          "nodeType": "JUNCTION",
          "elevationM": 8.35,
          "maxDepthM": 3.5,
          "initialDepthM": 0.0,
          "surchargeDepthM": 1.2,
          "pondedAreaM2": 20.0,
          "map": {
            "x": 3900.0,
            "y": 1223.0
          }
        },
        {
          "id": "comb_main_catch_basin_2_connector",
          "nodeType": "JUNCTION",
          "elevationM": 8.18,
          "maxDepthM": 2.6,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 4400.0,
            "y": 1223.0
          }
        },
        {
          "id": "overflow_chamber",
          "nodeType": "STORAGE",
          "elevationM": 7.75,
          "maxDepthM": 2.8,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 45.0,
          "map": {
            "x": 4752.0,
            "y": 1220.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "comb_main_2_manhole_to_catch_basin_2_segment",
          "linkType": "CONDUIT",
          "fromNode": "combined_manhole",
          "toNode": "comb_main_catch_basin_2_connector",
          "lengthM": 120.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.2,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.001417
        },
        {
          "id": "comb_main_2_downstream_segment",
          "linkType": "CONDUIT",
          "fromNode": "comb_main_catch_basin_2_connector",
          "toNode": "overflow_chamber",
          "lengthM": 70.0,
          "roughnessN": 0.015,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.2,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.006143
        }
      ]
    },
    {
      "htmlId": "overflow_chamber",
      "label": "우수토실-월류시설",
      "objectType": "overflow_facility",
      "system": "combined",
      "waterType": "combined",
      "swmmNodes": [
        "overflow_chamber",
        "overflow_normal_flow_node",
        "overflow_weir_outlet_node"
      ],
      "swmmLinks": [
        "overflow_normal_flow_gate",
        "overflow_excess_weir"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true,
        "operation": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "overflow_chamber",
          "nodeType": "STORAGE",
          "elevationM": 7.75,
          "maxDepthM": 2.8,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 45.0,
          "map": {
            "x": 4752.0,
            "y": 1220.0
          }
        },
        {
          "id": "overflow_normal_flow_node",
          "nodeType": "JUNCTION",
          "elevationM": 7.62,
          "maxDepthM": 2.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 4753.0,
            "y": 1054.0
          }
        },
        {
          "id": "overflow_weir_outlet_node",
          "nodeType": "JUNCTION",
          "elevationM": 7.7,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5012.0,
            "y": 1223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "overflow_normal_flow_gate",
          "linkType": "ORIFICE",
          "fromNode": "overflow_chamber",
          "toNode": "overflow_normal_flow_node",
          "orificeType": "SIDE",
          "offsetM": 0.2,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.95,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        },
        {
          "id": "overflow_excess_weir",
          "linkType": "WEIR",
          "fromNode": "overflow_chamber",
          "toNode": "overflow_weir_outlet_node",
          "weirType": "TRANSVERSE",
          "crestHeightM": 1.6,
          "qCoeff": 1.84,
          "gated": "NO",
          "crossSection": {
            "shape": "RECT_OPEN",
            "geom1": 1.0,
            "geom2": 2.4,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        }
      ]
    },
    {
      "htmlId": "overflow_to_interceptor_drop",
      "label": "우수토실 일반 유량에서 차집관거로 내려가는 관",
      "objectType": "pipe_group",
      "system": "combined",
      "waterType": "combined",
      "swmmNodes": [
        "overflow_chamber",
        "overflow_normal_flow_node",
        "overflow_interceptor_join"
      ],
      "swmmLinks": [
        "overflow_normal_flow_gate",
        "overflow_to_interceptor_drop"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "overflow_chamber",
          "nodeType": "STORAGE",
          "elevationM": 7.75,
          "maxDepthM": 2.8,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 45.0,
          "map": {
            "x": 4752.0,
            "y": 1220.0
          }
        },
        {
          "id": "overflow_normal_flow_node",
          "nodeType": "JUNCTION",
          "elevationM": 7.62,
          "maxDepthM": 2.8,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 4753.0,
            "y": 1054.0
          }
        },
        {
          "id": "overflow_interceptor_join",
          "nodeType": "JUNCTION",
          "elevationM": 5.65,
          "maxDepthM": 3.2,
          "initialDepthM": 0.0,
          "surchargeDepthM": 1.0,
          "pondedAreaM2": 20.0,
          "map": {
            "x": 4753.0,
            "y": 231.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "overflow_normal_flow_gate",
          "linkType": "ORIFICE",
          "fromNode": "overflow_chamber",
          "toNode": "overflow_normal_flow_node",
          "orificeType": "SIDE",
          "offsetM": 0.2,
          "qCoeff": 0.65,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.95,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        },
        {
          "id": "overflow_to_interceptor_drop",
          "linkType": "CONDUIT",
          "fromNode": "overflow_normal_flow_node",
          "toNode": "overflow_interceptor_join",
          "lengthM": 40.0,
          "roughnessN": 0.016,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 0.95,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 1.5,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.04925
        }
      ]
    },
    {
      "htmlId": "overflow_pipe",
      "label": "월류관",
      "objectType": "pipe_group",
      "system": "combined",
      "waterType": "overflow",
      "swmmNodes": [
        "overflow_chamber",
        "overflow_weir_outlet_node",
        "overflow_outfall_gate_node"
      ],
      "swmmLinks": [
        "overflow_excess_weir",
        "overflow_pipe"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "overflow_chamber",
          "nodeType": "STORAGE",
          "elevationM": 7.75,
          "maxDepthM": 2.8,
          "initialDepthM": 0.0,
          "shape": "FUNCTIONAL",
          "storageParam": 45.0,
          "map": {
            "x": 4752.0,
            "y": 1220.0
          }
        },
        {
          "id": "overflow_weir_outlet_node",
          "nodeType": "JUNCTION",
          "elevationM": 7.7,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5012.0,
            "y": 1223.0
          }
        },
        {
          "id": "overflow_outfall_gate_node",
          "nodeType": "JUNCTION",
          "elevationM": 6.3,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5870.0,
            "y": 1223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "overflow_excess_weir",
          "linkType": "WEIR",
          "fromNode": "overflow_chamber",
          "toNode": "overflow_weir_outlet_node",
          "weirType": "TRANSVERSE",
          "crestHeightM": 1.6,
          "qCoeff": 1.84,
          "gated": "NO",
          "crossSection": {
            "shape": "RECT_OPEN",
            "geom1": 1.0,
            "geom2": 2.4,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        },
        {
          "id": "overflow_pipe",
          "linkType": "CONDUIT",
          "fromNode": "overflow_weir_outlet_node",
          "toNode": "overflow_outfall_gate_node",
          "lengthM": 280.0,
          "roughnessN": 0.016,
          "inOffsetM": 0.0,
          "outOffsetM": 0.0,
          "initialFlowCms": 0.0,
          "maxFlowCms": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          },
          "losses": {
            "inletLoss": 0.0,
            "outletLoss": 0.0,
            "averageLoss": 0.0,
            "flapGate": "NO",
            "seepageRate": 0.0
          },
          "computedSlope": 0.005
        }
      ]
    },
    {
      "htmlId": "overflow_outfall",
      "label": "월류 방류구",
      "objectType": "outfall",
      "system": "combined",
      "waterType": "overflow",
      "swmmNodes": [
        "overflow_outfall_gate_node",
        "overflow_outfall"
      ],
      "swmmLinks": [
        "overflow_outfall_gate"
      ],
      "controls": {
        "rainfall": false,
        "blockage": true
      },
      "missingNodes": [],
      "missingLinks": [],
      "resolvedNodes": [
        {
          "id": "overflow_outfall_gate_node",
          "nodeType": "JUNCTION",
          "elevationM": 6.3,
          "maxDepthM": 2.4,
          "initialDepthM": 0.0,
          "surchargeDepthM": 0.5,
          "pondedAreaM2": 0.0,
          "map": {
            "x": 5870.0,
            "y": 1223.0
          }
        },
        {
          "id": "overflow_outfall",
          "nodeType": "OUTFALL",
          "elevationM": 6.25,
          "outfallType": "FREE",
          "gated": "NO",
          "map": {
            "x": 6028.0,
            "y": 1223.0
          }
        }
      ],
      "resolvedLinks": [
        {
          "id": "overflow_outfall_gate",
          "linkType": "ORIFICE",
          "fromNode": "overflow_outfall_gate_node",
          "toNode": "overflow_outfall",
          "orificeType": "SIDE",
          "offsetM": 0.0,
          "qCoeff": 0.75,
          "gated": "NO",
          "closeTimeSec": 0.0,
          "crossSection": {
            "shape": "CIRCULAR",
            "geom1": 1.8,
            "geom2": 0.0,
            "geom3": 0.0,
            "geom4": 0.0,
            "barrels": 1,
            "culvert": 0
          }
        }
      ]
    }
  ]
};
