-- Campaign Intent Stage Classification
-- Source: Growth research (Feb 2026), validated against dbt_analytics.fct_website_page_view
--
-- 4 intent stages based on campaign targeting and naming convention.
-- Each stage has its own KPI — do NOT judge TOF by order rate.
--
-- Usage: Include as CASE expression in any query joining dim_ads_campaign.campaign_name
--
-- KPI by stage:
--   1_Cold_Discovery:      Engaged visitor rate (30s+ engagement)
--   2_Active_Research:      200s+ deep engagement rate
--   3_Warm_Reengagement:    200s+ deep engagement rate
--   4_Purchase_Intent:      Commit chain (buy page → cart → order)

CASE
  -- 4: High Purchase Intent (brand search / Shopping)
  WHEN campaign_name ILIKE 'Bottom - shopping%' OR campaign_name ILIKE 'Bottom+-%shopping%' THEN '4_Purchase_Intent'
  WHEN campaign_name LIKE 'Bottom Search*Brand%' THEN '4_Purchase_Intent'
  WHEN campaign_name LIKE 'Sitelink%' THEN '4_Purchase_Intent'
  WHEN campaign_name LIKE 'Vibe_Bot_Search_Brand%' THEN '4_Purchase_Intent'

  -- 3: Warm Re-engagement (retargeting / remarketing)
  WHEN campaign_name ILIKE '%retargeting%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE '%remarketing%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE 'DG_AW_Retarget%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE 'DG_General_Biz_Website%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE 'bottomvideo%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE 'bottomdisplay%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE 'Bottom Display%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE 'BOF%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE 'Bottom_Purchase%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE '%Website Visitor%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE 'VideoRTL%' THEN '3_Warm_Reengagement'
  WHEN campaign_name LIKE 'StevenCase%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE 'EABF%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE 'Single Image%' THEN '3_Warm_Reengagement'
  WHEN campaign_name ILIKE 'Video - %' THEN '3_Warm_Reengagement'

  -- 2: Active Research (category / competitor search)
  WHEN campaign_name ILIKE 'HeadSmartboard%' THEN '2_Active_Research'
  WHEN campaign_name ILIKE 'HeadWhiteboard%' THEN '2_Active_Research'
  WHEN campaign_name ILIKE 'Middle Search%' THEN '2_Active_Research'
  WHEN campaign_name LIKE 'Search - VC%' THEN '2_Active_Research'
  WHEN campaign_name ILIKE 'Competitor%' THEN '2_Active_Research'
  WHEN campaign_name ILIKE 'Performance Max%' THEN '2_Active_Research'
  WHEN campaign_name ILIKE 'PMAX%' THEN '2_Active_Research'
  WHEN campaign_name LIKE 'Story_AI_for_Meeting%' THEN '2_Active_Research'
  WHEN campaign_name LIKE 'Story_Video_Conference%' THEN '2_Active_Research'

  -- 1: Cold Discovery (net new audience / industry targeting)
  WHEN campaign_name ILIKE 'Awareness%' THEN '1_Cold_Discovery'
  WHEN campaign_name ILIKE 'TOF%' THEN '1_Cold_Discovery'
  WHEN campaign_name ILIKE 'AEC%' THEN '1_Cold_Discovery'
  WHEN campaign_name ILIKE 'K12%' THEN '1_Cold_Discovery'
  WHEN campaign_name ILIKE 'Financial%Service%' THEN '1_Cold_Discovery'
  WHEN campaign_name ILIKE 'General%Biz%' THEN '1_Cold_Discovery'
  WHEN campaign_name ILIKE 'Higher%Education%' THEN '1_Cold_Discovery'
  WHEN campaign_name ILIKE 'Goverment%' THEN '1_Cold_Discovery'
  WHEN campaign_name LIKE 'Story_Fragmentation%' THEN '1_Cold_Discovery'
  WHEN campaign_name LIKE 'Story_Meeting%' THEN '1_Cold_Discovery'
  WHEN campaign_name LIKE 'Test_Client-facing%' THEN '1_Cold_Discovery'
  WHEN campaign_name LIKE 'SMB Owners%' THEN '1_Cold_Discovery'
  WHEN campaign_name ILIKE 'Legacy_%' THEN '1_Cold_Discovery'
  WHEN campaign_name ILIKE 'DG_ACE_TOF%' THEN '1_Cold_Discovery'
  WHEN campaign_name ILIKE 'DG_EDU_TOF%' THEN '1_Cold_Discovery'
  WHEN campaign_name LIKE 'DG_ACE(%' THEN '1_Cold_Discovery'
  WHEN campaign_name LIKE 'Entrepreneur%' THEN '1_Cold_Discovery'

  ELSE '5_Unclassified'
END as intent_stage
