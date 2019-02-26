# -*- coding: utf-8 -*-
import time
import logging
import scrapy

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from guahao_spider.items import CommentItem


class GuahaoSpider(scrapy.Spider):
    name = 'guahao'
    allowed_domains = ['guahao.com']
    login_url = 'https://www.guahao.com/user/login'
    #  start_url = 'https://www.guahao.com/hospital/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/1/all/all/all/0/false/order/p{}'
    #  start_url = 'https://www.guahao.com/hospital/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/all/all/all/all/0/false/7/p{}'
    #  start_url = 'https://www.guahao.com/hospital/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/p{}'
    start_url = 'https://www.guahao.com/hospital/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/all/33/all/all/0/false/region_sort/p{}'
    #  start_url = 'https://www.guahao.com/hospital/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/1/all/all/all/0/false/region_sort/p{}'

    #  comment_template_url = 'https://www.guahao.com/commentslist/h-{}/1-0?pageNo=1&sign=4C57CE49D28160821F8F746581C5AE62B390D283A43F3CA2C0D00977F19B36DA3998E934AEE1CA2A839CBDA0DAF11EEC889477289C283BDA20C8D75096DB67F8&timestamp=1550890253700'
    comment_template_url = 'https://www.guahao.com/commentslist/h-{}/1-0'
    hospital_ids = [
        #  '17634310-b567-4d21-8a02-20dc15e90da5000',
        'dde98fc9-4183-48ee-8c84-453058fa7fe3000',
        '5cee04f9-4cc8-4499-a35b-6f37f2dd8a74000',
        #  '60cd2663-d69d-4f63-bc17-8618d6e5e609000',
        #  '34250b55-2a8b-474a-95e9-48150516d7a5000',
        #  'fb60b555-d22d-4229-b79c-ce9e96c82863000',
        #  '5d04ae45-d4f9-42d8-a7f2-8f25897e197d000',
        #  'a986c8d76-c720-11e1-913c-5cf9dd2e7135000',
        #  '8f113a19-eee7-47b8-9517-2ad069a2f57a000',
        #  '448f9a19-8cd2-4ccf-a152-3930ec622d9f000',
        #  '986c9800-c720-11e1-913c-5cf9dd2e7135000',
        #  '125361059609302000',
        #  '9ff45a91-1e70-4fa5-b0af-2cd51d559a91000',
        #  '08991199-fee5-48cc-b827-95eb0fdbd980000',
        #  '05ba2f6c-ec92-4a58-a6d0-31befb5474ed000',
        #  '137228411103168000',
        #  '8cda804a-9de1-48cb-b99a-08c0c3e4672d000',
        #  '6d71e862-8cbc-4b92-b7de-db272d9e53c3000',
        #  '3b79d438-b0c8-436f-8e11-2f3120be91cf000',
        #  '9869d542-c720-11e1-913c-5cf9dd2e7135000',
        #  'f981627f-aa7e-40a7-9999-895377aa2031000',
        #  '73b2d4d7-6604-471a-8f2b-4efe6bb3ce35000',
        #  '253aa3fe-45ea-45e0-976b-c49ee58b92fb000',
        #  '125336754304601000',
        #  '128229647014009000',
        #  'eba8a3ab-dcde-4538-9a7e-05c55732b5f8000',
        #  '125336131920301000',
        #  'ce1fa639-29f5-4443-a76c-2006e445206e000',
        #  'a37ef412-f31e-421d-a291-2521ea6f74d8000',
        #  'BF314EAD23323ED3E040007F01004B66000',
        #  '4ed5457b-721f-4d81-bcf6-b018234886b2000',
        #  '70e69226-fcde-4c4b-9e0b-05802890863c000',
        #  '08991199-fee5-48cc-b827-95eb0fdbd980000',
        #  '1ee21b16-9630-4e97-b4d6-daa6218b4c98000',
        #  '138872494057004000',
        #  '8888a69d-5648-4710-99dd-92ee5e2ef1fe000',
        #  '6d71e862-8cbc-4b92-b7de-db272d9e53c3000',
        #  '136400854463027000',
        #  'DC2F8A126980DCE4E040A8C00F012A34000',
        #  'd4b40a10-5f19-458a-b5e4-8273597be106000',
        #  '64f9440a-dda7-4219-af06-cad2815359c2000',
        #  'a8d8d82e-7b49-496c-8dd7-fe8989d79bb4000',
        #  'c1623fc3-1926-44df-9de4-1562c162add9000',
        #  'f226027e-7533-4834-b790-40f205e42ad5000',
        #  '141135273808672000',
        #  'f3869b07-efad-4620-aeed-25d64c752155000',
        #  'a6990521-a9a0-435f-9f90-45f4dca3fb22000',
        #  '64f9440a-dda7-4219-af06-cad2815359c2000',
        #  '137228411103168000',
        #  '08319D6686C53137E0530F01A8C095E4000',
        #  '103f8180-abfd-4488-b5c7-dd7ad39e97a6000',
        #  'fb60b555-d22d-4229-b79c-ce9e96c82863000',
        #  'e66ec01e-3092-4425-a886-f5a980841538000',
        #  '139288285358051000',
        #  'd05c3dbe-3447-4a40-8381-badde169cd03000',
        #  '986d3f86-c720-11e1-913c-5cf9dd2e7135000',
        #  '9e592a81-4b29-4298-bcaf-65848b052b85000',
        #  '2a04d236-c2df-4914-a10f-35d81db31f1e000',
        #  '2c272db5-1798-477a-b313-4d7374f7467d000',
        #  '128796908419696000',
        #  'af25fd28-0a0c-415a-b00a-24f1d4405b3c000',
        #  '548d9ae3-d56d-4f53-a35a-cbd0cb7c9923000',
        #  '8c8a90ec-75de-40c2-9a25-11511ff9fc3e000',
        #  'b32c9311-84fa-492e-a5f5-d9dc802aa0c8000',
        #  'BF314EAD23383ED3E040007F01004B66000',
        #  '4c43f88b-425b-48fa-838a-ef8f54113146000',
        #  '9743eeb5-96ba-484e-b60c-51fe2af48a41000', # p12
        #  'ad3ff46d-ea7f-4d5a-a8ef-76c05048e571000',
        #  '986c0e05-c720-11e1-913c-5cf9dd2e7135000',
        #  '139659138736903000',
        #  '1abfe584-d7de-4ad4-a345-faa1fc492960000',
        #  '8296304b-5550-4c20-a434-97e82e19b45e000',
        #  'c102e248-751a-4d0b-941d-94a2c33a4e0b000',
        #  '138716556639136000',
        #  'e4d827d9-9175-410d-b6ea-108984eca121000',
        #  'e75a2ad0-72c5-425b-9b36-34a8dc16a485000',
        #  '986d718f-c720-11e1-913c-5cf9dd2e7135000',
        #  '142232405598617000',
        #  '986c5f83-c720-11e1-913c-5cf9dd2e7135000',
        #  '137228411106872000',
        #  'ED25EA3F3EE9A102E040A8C00F01221B000',
        #  '6d6ca698-e799-4fd9-b0c1-8a086f1f134f000',
        #  'FEC007C4EC021EF0E040A8C00F012C86000',
        #  'BF314EAD231F3ED3E040007F01004B66000',
        #  'eb5163f2-c2c8-4a58-af7e-4a1350a163f1000',
        #  '986d41c1-c720-11e1-913c-5cf9dd2e7135000',
        #  '5ff89d5d-5f01-4945-b687-fa47662fd5aa000',
        #  'ca75a626-94c2-44f5-920d-f81781ab3939000',
        #  '9d8c1b10-78bf-4d44-9d27-bd9efbafed9e000',
        #  '137327271169128000',
        #  '9b5f86a4-ca22-4c29-96eb-59dfb21c70ca000',
        #  '86428123FC77499A9ED1358DB486CFF7000',
        #  '140289995097803000',
        #  'bda8c618-487e-4f9a-9b99-0ab29f88a407000',
        #  '9d09929b-e7ae-446c-a169-5a65daa4f51b000',
        #  '561b78b0-927d-4de7-94b5-45d270d73a15000',
        #  '45141a4d-3d76-4647-bc17-93684b4d9ec9000',
        #  '9fad6711-dfc9-4d05-8968-2da2bd1cc170000',
        #  '986c5b78-c720-11e1-913c-5cf9dd2e7135000',
        #  '875ad940-e765-4343-a1fc-ae65e5673ff1000',
        #  'ff739ebb-4c24-43bc-af4d-c5356b10db91000',
        #  '137228411108180000',
        #  '97b79f8e-28c1-4603-9f57-b141f8a2657b000',
        #  '3b79d438-b0c8-436f-8e11-2f3120be91cf000',
        #  '986c5ed4-c720-11e1-913c-5cf9dd2e7135000',
        #  'FF0153A8EF402010E0430F01A8C07495000',
        #  '9ebb183d-54d9-4b10-a852-567b930dd7e3000', # p15
        #  '986d8a43-c720-11e1-913c-5cf9dd2e7135000',
        #  'b88ada3d-1d71-4492-ba04-19d8167e6b04000',
        #  '050C994FAE019340E0500A0AC8645D53000',
        #  '55bdac9f-d8e7-4796-950a-f62c47d69b89000',
        #  'ccb59b2f-027d-489c-888d-7577dc95558f000',
        #  'BF314EAD231E3ED3E040007F01004B66000',
        #  '2ce5bade-0de3-46ad-9d45-2111330dbbe1000',
        #  '139718209241750000',
        #  '9868f766-c720-11e1-913c-5cf9dd2e7135000',
        #  '4c6ac257-20c5-4166-94eb-41ab1fb3edaa000',
        #  '986d27c0-c720-11e1-913c-5cf9dd2e7135000',
        #  '12d9da15-a48a-4d6c-8ede-ba4596d3fe8b000',
        #  '42be4882-cb5f-4f96-8f42-6d921c063b27000',
        #  '2b0d6644-f927-489e-84c3-bfbea0b74f45000',
        #  'a25c8e22-a779-4866-bc50-3b6ae67fbe36000',
        #  '0282eb23-2890-4a4a-94ff-76050e960b2e000',
        #  '650d530f-f856-4655-a301-13c40a44c43f000',
        #  '75aabd65-9639-4984-8509-ec19c931b684000',
        #  'b0075dcd-39c2-4385-8c2e-f01d2e5fbe5e000',
        #  'ED25EA3F3F65A102E040A8C00F01221B000',
        #  '6994072d-6444-4eca-a6ea-cd8909f8119a000',
        #  '8a30b141-ff83-4ec2-ad79-5005ee3964b7000',
        #  'D12F17CF04B6EDADE040A8C0790231D2000',
        #  '4e5ce9e5-a66c-4060-818f-57ab5eaec590000',
        #  'FF0153A8EF3A2010E0430F01A8C07495000',
        #  '8dacdbb8-b998-4a84-91ff-2e7dd018a70d000',
        #  '986d6aeb-c720-11e1-913c-5cf9dd2e7135000',
        #  '90cce8d6-6241-4da4-920f-0ca10e4e0137000',
        #  '986d04f0-c720-11e1-913c-5cf9dd2e7135000',
        #  '75eab779-3179-45af-a0c0-c69c9e04148b000',
        #  '131951542818325000',
        #  '8aa13d0c-138a-4d9b-bbd8-1f2e780d7db2000',
        #  '986bcf4f-c720-11e1-913c-5cf9dd2e7135000',
        #  '2ad8bb1d-bcb9-49b3-870b-1c9d5be60bbe000',
        #  '12635601-8d9e-44e4-becd-1076d04c5795000',
        #  'd8f6d3b1-72a9-43b4-84b1-179740a1512e000',
        #  'A925DC393D8D47AFB4FE4E6847DD5989000',
        #  '138681870014210000',
        #  '6a994aa2-500f-4470-a911-27d646cc532a000',
        #  'EDB440F681F15790E0400A0AC86438BF000',
        #  '1e84204e-8f20-4790-a110-d41701209412000',
        #  '2425d2e5-06a3-4389-a739-98ac0e3f0c2f000',
        #  '0bf1e30c-385e-4b24-92ee-724d9e23582c000',
        #  '0553f8e2-0846-4874-b9f8-93ed09b4fc1c000',
        #  '140668519213518000',
        #  '9869d542-c720-11e1-913c-5cf9dd2e7135000',
        #  '71342d44-fd7b-4265-8240-e224e5f98c40000',
        #  '9868b760-c720-11e1-913c-5cf9dd2e7135000',
        #  'c0d3a004-12bc-4033-a555-222b117615fa000',
        #  'e2cbe59c-369f-48f5-9f56-cbdd46f6de7e000',  # p20
        #  'c238c98e-74a0-4047-ae89-b9e0685062f1000',
        #  '3a968a19-d337-47f2-97c5-339b2e069d3f000',
        #  'ace4c780-68be-4fc4-85d5-f46fdf1fffd4000',
        #  '06e0a487-3ded-424d-91f5-e64b65cb772c000',
        #  'bba5524b-fa4a-4aaf-b962-d47333a6a9f8000',
        #  'c17d464e-20b3-4bf8-a383-b9b51f916e05000',
        #  'ebfe1148-07a6-4d00-a920-73bec2b4f4d1000',
        #  '986c420b-c720-11e1-913c-5cf9dd2e7135000',
        #  '986d88c6-c720-11e1-913c-5cf9dd2e7135000',
        #  'e78b3e7b-2b68-4e5c-b5f3-399c650b45e5000',
        #  '9867cedb-c720-11e1-913c-5cf9dd2e7135000',
        #  '986a373a-c720-11e1-913c-5cf9dd2e7135000',
        #  'BF429DB051B6CC22E040007F010012AE000',
        #  '986c799a-c720-11e1-913c-5cf9dd2e7135000',
        #  '137228411107174000',
        #  'FEC007C4EB741EF0E040A8C00F012C86000',
        #  '25625a41-0edd-40d8-a06e-6e51d961e2b7000',
        #  'c0b18885-5416-4c4a-a4d6-9fc4e6933ba8000',
        #  '986d2e97-c720-11e1-913c-5cf9dd2e7135000',
        #  '9a995811-c720-11e1-913c-5cf9dd2e7135000',
        #  '986d70f3-c720-11e1-913c-5cf9dd2e7135000',
        #  'e8604864-034c-4277-8c08-1f314752f215000',
        #  '9867ea6c-c720-11e1-913c-5cf9dd2e7135000',
        #  'EDDECCA828DAE72AE0400A0AC8642357000',
        #  '986c329b-c720-11e1-913c-5cf9dd2e7135000',
        #  'FF0153A8EFFD2010E0430F01A8C07495000',
        #  '986ae054-c720-11e1-913c-5cf9dd2e7135000',
        #  'c17e65ad-8ab0-43ab-93f0-ca7d234db04a000',
        #  '986c5648-c720-11e1-913c-5cf9dd2e7135000',
        #  '6c91b962-f190-4a9b-bf38-6a2ce61c9c5b000',
        #  '137905381138489000',
        #  'ce2c7631-8371-416c-9654-2ffeaa66520d000',
        #  '5DA21D26520947EC831FE0F887E75563000',
        #  'd58e7974-9e01-4b36-9ab7-082f5327385b000',
        #  '138138211148208000',
        #  '9869c1db-c720-11e1-913c-5cf9dd2e7135000',
        #  '137569773838227000',
        #  'db48e2dd-ff1e-46a5-abe6-af9f9e44d36c000',
        #  '3eded5c6-e446-4c3d-8068-650df181abba000',
        #  '986b134f-c720-11e1-913c-5cf9dd2e7135000',
        #  '137228411109186000',
        #  '777e62b3-6e97-4baa-b155-8adf5d899cc6000',
        #  '986d22e6-c720-11e1-913c-5cf9dd2e7135000',
        #  '986d2086-c720-11e1-913c-5cf9dd2e7135000',
        #  '5d72eae7-2baf-4597-a807-37302f4464ca000',
        #  '367fd7d4-e91b-4602-913a-8b7439a6f28b000',
        #  '16bf6c3d-f5a4-49bf-ba42-d961b831f8e3000',
        #  '592AAA6506214DA6BDAA910210474C75000',
        #  '51e5fdae-6049-4638-ac87-c3184d8880c2000',
        #  'be7fff6a-94f5-421d-96e3-6750100ef97b000',
        #  'c6c30b5e-14f1-499e-ba40-809b6f2a2953000',
        #  '986bd4cf-c720-11e1-913c-5cf9dd2e7135000',
        #  '986d2149-c720-11e1-913c-5cf9dd2e7135000',
        #  'b754c322-485f-40d4-9104-1fb9610acdd4000',
        #  '140566830063228000',
        #  '9a91016b-c720-11e1-913c-5cf9dd2e7135000',
        #  '582d4265-0891-472e-ad66-2d59546709fc000',
        #  '8a12f216-75e4-44a9-835d-39d801a49582000',
        #  '9cb6c0ac-aa21-4251-9e9f-326a2d200073000',
        #  'ef837ad9-a2d8-41e0-8c1e-91b7e6fe6ab8000',
        #  '986c77b9-c720-11e1-913c-5cf9dd2e7135000',
        #  '6a36ff98-f9e3-4a2f-9feb-8d08236c68e9000',
        #  '986d1f02-c720-11e1-913c-5cf9dd2e7135000',
        #  '02d76d98-2471-4a91-9f89-198833b948c3000',
        #  '986c2002-c720-11e1-913c-5cf9dd2e7135000',
        #  '986bd861-c720-11e1-913c-5cf9dd2e7135000',
        #  '9867f3eb-c720-11e1-913c-5cf9dd2e7135000',
        #  '7343d4ce-c876-4d31-80eb-3691c6aaaf9c000',
        #  '3d30af33-3c9c-43c3-b136-9152e8ece1f4000',
        #  'cf460b90-30e0-4894-8dfc-1f6d1cf6b36d000',  # p27
        #  '141647084028526000',
        #  'ac739332-eaaa-469a-9c67-04fa0b684ad9000',
        #  '902df64d-b0d3-4a88-a229-eb015c5c0f41000',
        #  '137228411107576000',
        #  'fadbc010-ed25-4e20-8580-0199e87e95be000',
        #  '139591057953884000',
        #  'd1dcf605-f86a-4f2c-a554-58cc3bd292c2000',
        #  '986acb11-c720-11e1-913c-5cf9dd2e7135000',
        #  'fa3134ba-a02c-4035-8103-34f8b119c643000',
        #  '08C006A09457FA88E0500A0AC8641E3E000',
        #  '9a9a16cd-c720-11e1-913c-5cf9dd2e7135000',
        #  '19cdd4f7-3bf2-447a-b337-c5b737fde0c5000',
        #  'bddce032-c9fa-49f3-b0f8-50e81aff1c6a000',
        #  'edce8488-b52e-4389-a6e7-856d19f8b44b000',
        #  '140963940432110000',
        #  'ca4317bc-4274-4b5c-91bb-447e743d4956000',
        #  '3a4cd718-8744-4293-959d-f2c3942afe25000',
        #  '897232f5-0be4-4914-9f9b-40b2641fb2d8000',
        #  '11181afd-e048-4963-a2f7-64747e05e651000',
        #  '986b10c4-c720-11e1-913c-5cf9dd2e7135000',
        #  '2a5f0396-505f-4b03-bf41-14e1d54e4f04000',
        #  '9867423d-c720-11e1-913c-5cf9dd2e7135000',
        #  '138871376955754000',
        #  'd693fdaa-1e6b-4a8c-a8c1-aab7a2468347000',
        #  '8998f924-d633-495c-8f7a-eaea0dfee1d4000',
        #  '821f1264-907c-4e13-b772-f3403a149436000',
        #  '98684eaf-c720-11e1-913c-5cf9dd2e7135000',
        #  '86484bde-21d4-4ad2-a72b-27119250a840000',
        #  '986b58f8-c720-11e1-913c-5cf9dd2e7135000',
        #  '137905381139593000',
        #  'b54f9d4b-eed7-4d82-96c1-0f7893a6ffba000',
        #  'bfc116f1-437a-4557-98bc-392f72c7dcae000',
        #  '9869d7a5-c720-11e1-913c-5cf9dd2e7135000',
        #  '9867ce50-c720-11e1-913c-5cf9dd2e7135000',
        #  '17d8d2e1-8f29-42e2-826b-0f76e7806fd7000',
        #  '9fcc0c65-d1a8-4e8e-a0f4-68c2dac49bfa000',
        #  'FEC007C4E9DA1EF0E040A8C00F012C86000',
        #  'f1bb6f71-a795-415a-ba5b-5cf977e8028a000',
        #  'CDE27F434D83C329E040A8C079023B55000',
        #  '1c17553f-1245-44bf-846e-a2b23969c7ac000',
        #  '138681919758805000',
        #  'a71cc150-a679-4df8-893c-3a4baa7f2f3e000',
        #  '6154afee-a134-495b-809b-0d5249471260000',
        #  '9867e2b5-c720-11e1-913c-5cf9dd2e7135000',
        #  '9a8a326e-c720-11e1-913c-5cf9dd2e7135000',
        #  'd12ffdae-1dae-41e4-8455-8e0226533e7a000',
        #  'a58f12b9-6c9e-4cdf-a818-7cf48e708ec6000',
        #  'e1362c5f-e266-4126-92c7-4cd26a7cf1ad000',
        #  '6f078400-9510-49a5-abf8-c6390c37aadd000',
        #  '9a99af1a-c720-11e1-913c-5cf9dd2e7135000',
        #  'a0632bb9-b2ff-4987-8373-0cdef468f6e7000',
        #  '141647113515718000',
        #  '70167259-006f-43b0-ae7c-b93703fa77e7000',
        #  '9868c72e-c720-11e1-913c-5cf9dd2e7135000',
        #  '986d6720-c720-11e1-913c-5cf9dd2e7135000',
        #  '8efb333b-91ac-48fa-b4a2-3e6985023537000',
        #  '61f778a6-6f37-4fe2-b7d0-20fb1870bcbf000',
        #  '3b3121de-9265-4f34-9746-bab96806c880000',
        #  '633686f2-0763-4247-94e4-33ecc9e89d4f000',
        #  '986c3710-c720-11e1-913c-5cf9dd2e7135000',
        #  '986d3089-c720-11e1-913c-5cf9dd2e7135000',
        #  '4cb5d020-bf13-47b7-b0b1-e5a26a48bc5d000',
        #  '8d7665a0-ad57-4114-aa4d-09aa3bd20078000',
        #  '138623336233807000',
        #  'ED25EA3F3F5BA102E040A8C00F01221B000',
        #  '9869b07f-c720-11e1-913c-5cf9dd2e7135000',
        #  'f427b6aa-aec3-443d-9865-8b7a65e77298000',
        #  '140074969728830000',
        #  '2da7cf44-4969-4fde-a7b9-3500263e5743000',
        #  '137228411108482000',
        #  '986b2106-c720-11e1-913c-5cf9dd2e7135000',
        #  'f4dcf770-acb0-40c9-979b-97c141f3ccef000',
        #  '08a48932-bf29-4cc7-bc57-7e7e58f6f6a5000',
        #  'f9f0e8ab-0b39-43d4-8f26-0b7ba0a7ae15000',
        #  '8e48f4bf-bc26-40bb-a7c2-e7e566a48233000',
        #  '139400118051740000',
        #  '98674a8b-c720-11e1-913c-5cf9dd2e7135000',
        #  '9a505d07-4516-46c6-8bea-de3ced809d3e000',
        #  '986ba7bd-c720-11e1-913c-5cf9dd2e7135000',
        #  'e67ebf30-88b8-4a57-8d63-3b790ef999f1000',  # p35
        '36189D9C2965454F8C24B71E6A5BBC5F000',
        '137905381139091000',
        'cbb10df2-ae84-44d8-8b92-0d5f439636d6000',
        'b9b7dde3-9fa3-4452-95bd-87453c931a7d000',
        '233b70e3-78b3-4eba-b770-98f41aa1eede000',
        '25e74836-1225-4705-bd7c-91b5f4e238aa000',
        'BF42114847F803BDE040007F01006031000',
        '24a00b5b-fc08-45ba-876a-1f714b5a34d5000',
        '98685546-c720-11e1-913c-5cf9dd2e7135000',
        '986c33dc-c720-11e1-913c-5cf9dd2e7135000',
        '879765ed-757c-40bd-a5ad-a44e07f60c56000',
        '9a998176-c720-11e1-913c-5cf9dd2e7135000',
        'BF429DB0519CCC22E040007F010012AE000',
        'b7b117e3-2b6f-4125-b289-f08d698cc4c9000',
        '986957b0-c720-11e1-913c-5cf9dd2e7135000',
        '560aafc4-41a4-4b2f-bb58-426168f63d32000',
        '4e195d5e-e354-47bf-bd64-fd3ee107c3a8000',
        '98682e12-c720-11e1-913c-5cf9dd2e7135000',
        '9869ff92-c720-11e1-913c-5cf9dd2e7135000',
        '986c4156-c720-11e1-913c-5cf9dd2e7135000',
        'd607e085-72a5-4fa1-af68-2f1767d6d47f000',
        'BF429DB051BFCC22E040007F010012AE000',
        'EBC03AF758A9AEABE0400A0AC8647824000',
        'BF42114847F503BDE040007F01006031000',
        '986d6f0d-c720-11e1-913c-5cf9dd2e7135000',
        '9a99881c-c720-11e1-913c-5cf9dd2e7135000',
        '66fdb685-648f-4071-84d4-654282cfb35a000',
        '8200f2a5-e933-4a31-929a-f0ea8c2dcf9a000',
        '986a88e9-c720-11e1-913c-5cf9dd2e7135000',
        'fe54ca19-39c7-403b-baae-ce55d34e2e5d000',
        'EDB440F6810D5790E0400A0AC86438BF000',
        'a7463b63-0f44-4b7b-bae2-d0a36ec5e40f000',
        'af8ad711-1cab-48d5-a4d4-e92d387cf825000',
        '986d6e05-c720-11e1-913c-5cf9dd2e7135000',
        '3203aee3-c9a9-4b5e-a71e-c40fd787a63f000',
        '67a85484-b12c-4283-9e4a-a432b447d25b000',
        '2f5c017c-3877-471b-83f4-eda43fc2542c000',
        '9868c6a5-c720-11e1-913c-5cf9dd2e7135000',
        'a0acb0fc-f0f0-4132-b905-33268abfde47000',
        'e0446d33-516f-438a-a78b-bb824a4bdba2000',
        'a0d6093c-d8e3-4bf1-b990-09b304c93085000',
        '9a92ab9e-c720-11e1-913c-5cf9dd2e7135000',
        '8c0224d8-c804-496d-b04c-87d1e0f54e5c000',
        '83017cc6-f325-4b22-9a18-4ecf2b62170b000',
        '98686e55-c720-11e1-913c-5cf9dd2e7135000',
        'c239960f-2883-4d40-a3a8-9a4edbd5af26000',
        '9a912d15-c720-11e1-913c-5cf9dd2e7135000',
        '986782a5-c720-11e1-913c-5cf9dd2e7135000',
        'ecce0df7-c7b3-4135-bc65-5ec1bcdb3142000',
        '138871194479745000',
        '138683098076697000',
        '3e250c80-e1ea-422a-add1-9518d7176abf000',
        '4d7c5556-70d6-41b4-abbb-90a4f95892d1000',
        'ae0ebf49-6d1d-440d-a9de-aa69cb6da053000',
        '137228411109488000',
        '8b9ecbce-844f-46f8-86df-d89e9a2da070000',
        'f4bbc423-e52c-4ac0-be01-ccb22626802d000',
        'acd88f81-36c6-4f0e-8155-150b16244f61000',
        '75bbf1b6-6a32-40b5-8ce1-b89019127e15000',
        '9868c381-c720-11e1-913c-5cf9dd2e7135000',
        '5cc9205b-f6e5-4f99-9bbd-a12bb47715da000',
        'ae95f714-27ef-449a-8787-62086e8f99a9000',
        'd7916af3-e2b4-4573-89fc-de6a918c8d35000',
        '6f339869-be60-42ff-9766-29522ba81739000',
        '05010a0e-d110-4720-9d7e-d9bdd8c5d261000',
        '02a29335-dca2-48ee-ac08-9234ef824784000',
        '986c4660-c720-11e1-913c-5cf9dd2e7135000',
        '0a77e58f-6282-4421-88bf-1a0f383b6034000',
        '04eae929-4174-481c-8e15-3a4cd946c7f5000',
        '9a911135-c720-11e1-913c-5cf9dd2e7135000',
        '986d8c7d-c720-11e1-913c-5cf9dd2e7135000',
        '9869d4ae-c720-11e1-913c-5cf9dd2e7135000',
        '9869dfc9-c720-11e1-913c-5cf9dd2e7135000',
        'FF0153A8EB462010E0430F01A8C07495000',
        'f9d96eca-1a13-41b7-8431-397aa3c9a6ce000',
        '17c711b9-b61b-4ac3-af3a-1d9bdb43ab2f000',
        'aa8b36f4-458f-4c04-aff2-a32998b86bae000',
        'e38d7128-905b-42e4-aaa4-22f9e5800579000',
        '142129333351967000',
        '986bcc04-c720-11e1-913c-5cf9dd2e7135000'  # p43

    ]

    min_page = 1  # 21
    max_page = 15  # 91

    def __init__(self):
        self.driver = webdriver.Firefox()
        #  self.driver = webdriver.Chrome()
        self.hospital_set = set()
        pass

    def start_requests(self):
        logging.info('start_request.............')
        """This function is called before crawling starts."""

        #  yield SeleniumRequest(
        #  url=self.login_url,
        #  callback=self.start_crawl,
        #  wait_time=10,
        #  wait_until=EC.element_to_be_clickable((By.ID, 'gh'))
        #  )

        self.driver.get(self.login_url)
        element = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "gh"))
        )
        for hospital_id in self.hospital_ids:
            hospital_comment_url = self.comment_template_url.format(
                hospital_id)
            yield scrapy.Request(hospital_comment_url, cookies=self.driver.get_cookies(), callback=self.parse_comment)

        """
        for page_num in range(self.min_page, self.max_page):
            url = self.start_url.format(page_num)
            #  time.sleep(1)
            #  yield SeleniumRequest(url=url, callback=self.parse)
            yield scrapy.Request(url, cookies=self.driver.get_cookies(), callback=self.parse)

        """

        """
        first_page = self.start_url.format(self.min_page)
        yield scrapy.Request(first_page, cookies=self.driver.get_cookies(), callback=self.parse)

        """

    def parse(self, response):
        logging.info('-----------> parse, response url: %s, code: %s' %
                     (response.url, response.status))

        if response.url.find('commentslist') != -1:
            #  yield scrapy.Request(url=response.url, cookies=self.driver.get_cookies(), callback=self.parse_comment)
            yield scrapy.Request(response.url, callback=self.parse_comment)
            #  yield SeleniumRequest(url=response.url, callback=self.parse_comment)

        # hospital list
        hospital_list = response.xpath(
            '//ul[@class="hos_ul"]/li[contains(@class, "g-hospital-item")]')

        if hospital_list is not None and len(hospital_list) > 0:
            #  logging.info('len(hospital_list): ', len(hospital_list))
            for hospital in hospital_list:
                hospital_url = hospital.xpath(
                    'a[contains(@class, "cover-bg")]/@href').extract_first()
                hospital_id = hospital_url.split('/')[-1]

                hospital_comment_url = self.comment_template_url.format(
                    hospital_id)
                #  yield scrapy.Request(url=hospital_comment_url, cookies=self.driver.get_cookies(), callback=self.parse_comment)
                yield scrapy.Request(hospital_comment_url, callback=self.parse_comment)

        """

        cur_page = response.xpath(
            '//div[@class="papers"]/span[@class="current"]/text()').extract_first()
        if cur_page is None:
            cur_page = response.xpath(
                '//*[@id="g-cfg"]/div[1]/div[4]/div/form/div[1]/span/text()').extract_first()

        #  logging.info('cur_page ------------------> : %s' % cur_page)
        #  if cur_page is not None and int(cur_page) <= self.max_page:
        if cur_page is not None:
            nex_page = int(cur_page) + 1

            next_page_url = self.start_url.format(nex_page)
            logging.info('next_page_url ------------------> : %s' %
                         next_page_url)

            #  yield scrapy.Request(next_page_url, cookies=self.driver.get_cookies(), callback=self.parse)
            yield scrapy.Request(next_page_url, callback=self.parse)
        """

    def parse_comment(self, response):
        #  if response.url.find('commentslist') == -1:
            #  yield scrapy.Request(url=response.url, cookies=self.driver.get_cookies(), callback=self.parse)
        logging.info('parse_comment-----------> url: %s, code: %s' % (response.url, response.status))
        # selenium get
        self.driver.get(response.url)
        try:
            next_page = self.driver.find_element_by_xpath('//div[@class="g-pagination"]/div/form/div[@class="pagers"]/a[contains(@class, "next")]')
        except NoSuchElementException as e:
            next_page = None

        items = list()

        try:
            hospital_name = str(self.driver.find_element_by_xpath('//h1/strong/a').text)

            hospital_grade = str(self.driver.find_element_by_xpath('//h1/span').text)
            hospital_grade = hospital_grade.replace(
                '\n', '').replace('\t', '').replace(' ', '')
        except Exception as e:
            hospital_name = '无'
            hospital_grade = '无'

        while next_page is not None:
            try:
                logging.info('current url -----------------> : %s' % self.driver.current_url)
                comment_lis = self.driver.find_elements_by_xpath('//ul[@id="comment-list"]/li')
                for comment_li in comment_lis:
                    try:
                        item = CommentItem()

                        row1_ps = comment_li.find_elements_by_xpath('.//div[@class="row-1"]/p')
                        #  logging.info('len(row1_ps) -----------------> : %s' %

                        # disease name
                        try:
                            disease = str(
                                row1_ps[0].find_element_by_xpath('.//span').text)
                            disease = disease.replace('\n', '').replace(
                                '\t', '').replace(' ', '')
                        except NoSuchElementException as e:
                            disease = '无'
                            logging.info(e)
                        #  logging.info('disease -----------------> : %s' % disease)

                        # score
                        score = str(len(row1_ps[1].find_elements_by_xpath(
                            './/span[contains(@class, "giS-star-0")]')))
                        #  logging.info('score -----------------> : %s' % score)

                        row2_divs = comment_li.find_elements_by_xpath(
                            './/div[@class="row-2"]/div')

                        # comment text
                        try:
                            text = row2_divs[0].find_element_by_xpath('.//span[@class="detail"]')
                        except NoSuchElementException as e:
                            text = row2_divs[0].find_element_by_xpath('.//span[@class="summary"]')
                        text = str(text.text)
                        #  logging.info('text -----------------> : %s' % text)

                        # comment date
                        date = row2_divs[1].find_element_by_xpath('.//p/span[1]')
                        date = str(date.text.split()[-1][1:-1])

                        # doctor
                        try:
                            doctor = row2_divs[1].find_element_by_xpath(
                                './/p/span[2]/a')
                            doctor = str(doctor.text)
                        except NoSuchElementException as e:
                            doctor = '佚名'
                        #  logging.info('doctor -----------------> : %s' % doctor)

                        item['hospital_name'] = hospital_name
                        item['hospital_grade'] = hospital_grade

                        item['disease'] = disease
                        item['text'] = text
                        item['score'] = score
                        item['date'] = date
                        item['doctor'] = doctor

                        items.append(item)
                    except Exception as e:
                        logging.info(
                            'item error -----------------------> {}'.format(e))
                        logging.info('item: {}'.format(item))
                        continue
                try:
                    next_page = self.driver.find_element_by_xpath('//div[@class="g-pagination"]/div/form/div[@class="pagers"]/a[contains(@class, "next")]')
                except NoSuchElementException as e:
                    next_page = None

                next_page.click()
                time.sleep(0.30)
            except Exception as e:
                logging.info('next page error -------------------> {}'.format(e))
                continue

        logging.info('len(items) -----------------> : %d' % len(items))
        for item in items:
            yield item

        """
        hospital_name = response.xpath('//h1/strong/a/text()').extract_first()
        if hospital_name is None:
            hospital_name = response.xpath(
                '//*[@id="hospital-card-inner"]/div[1]/div[2]/h1/strong/a/text()').extract_first()
        if hospital_name is None:
            hospital_name = '佚名'
        hospital_name = hospital_name.replace(
            '\n', '').replace('\t', '').replace(' ', '')

        hospital_grade = response.xpath('//h1/span/text()').extract_first()
        if hospital_grade is None:
            hospital_grade = response.xpath(
                '//*[@id="hospital-card-inner"]/div[1]/div[2]/h1/span[1]').extract_first()
        if hospital_grade is None:
            hospital_grade = '无等级'
        hospital_grade = hospital_grade.replace(
            '\n', '').replace('\t', '').replace(' ', '')

        comment_lis = response.xpath('//ul[@id="comment-list"]/li')
        for comment in comment_lis:
            #  try:
            item = CommentItem()
            disease = ''
            text = ''
            score = 0
            date = ''
            doctor = ''

            row1_ps = comment.xpath('div[@class="row-1"]/p')

            # disease name
            disease = row1_ps[0].xpath('span/text()').extract_first()
            if disease is None:
                disease = '无'
            disease = disease.replace('\n', '').replace(
                '\t', '').replace(' ', '')

            # score
            score = len(row1_ps[1].xpath(
                'span[contains(@class, "giS-star-0")]'))

            row2_divs = comment.xpath('div[@class="row-2"]/div')

            # comment text
            text = row2_divs[0].xpath(
                'span[@class="detail"]/text()').extract_first()
            if text is None:
                text = row2_divs[0].xpath(
                    'span[@class="summary"]/text()').extract_first()

            # comment date
            date = row2_divs[1].xpath(
                'p/span[1]/text()').extract_first().split()[-1][1:-1]

            # doctor
            doctor = row2_divs[1].xpath(
                'a[class="name"]/text()').extract_first()
            if doctor is None:
                doctor = response.xpath(
                    '//*[@id="comment-list"]/li[1]/div[3]/div[2]/p/span[2]/a/text()').extract_first()

            item['hospital_name'] = hospital_name
            item['hospital_grade'] = hospital_grade

            item['disease'] = disease
            item['text'] = text
            item['score'] = score
            item['date'] = date
            item['doctor'] = doctor

            yield item
            #  except Exception as e:
            #  logging.info('e: {}'.format(e))
            #  continue
        """

        """
        page_no = response.xpath(
            '//form[@name="qPagerForm"]/input[@name="pageNo"]/@value').extract_first()
        if page_no is None:
            page_no = response.xpath(
                '//*[@id="g-cfg"]/div[3]/div/div/section/div[2]/div[1]/div/form/div[1]/span/text()').extract_first()

        if page_no is None:
            page_no = response.xpath(
                '//*[@id="g-cfg"]/div[3]/div/div/section/div[2]/div[1]/div/form/input[1]/@value').extract_first()

        if page_no is not None:
            logging.info('current url -----------------> : %s' % response.url)

            logging.info('current page_no --------------> : %s ' % page_no)
            next_page_no = int(page_no) + 1
            logging.info('next_page_no--------------> : %d ' % next_page_no)

            # sign
            sign = response.xpath(
                '//form[@name="qPagerForm"]/input[@name="sign"]/@value').extract_first()
            if sign is None:
                sign = response.xpath(
                    '//*[@id="g-cfg"]/div[3]/div/div/section/div[2]/div[1]/div/form/input[2]/@value').extract_first()

            logging.info('sign--------------> : %s ' % sign)

            # timestamp
            timestamp = response.xpath(
                '//form[@name="qPagerForm"]/input[@name="timestamp"]/@value').extract_first()
            if timestamp is None:
                timestamp = response.xpath(
                    '//*[@id="g-cfg"]/div[3]/div/div/section/div[2]/div[1]/div/form/input[3]/@value').extract_first()

            logging.info('timestamp--------------> : %s ' % timestamp)
            """

        """
            if response.url.find('pageNo') != -1:
                next_url = response.url.split('pageNo')[0] + 'pageNo={}&sign={}&timestamp={}'.format(next_page_no, sign, timestamp)
            else:
                next_url = response.url + '?pageNo={}&sign={}&timestamp={}'.format(next_page_no, sign, timestamp)
            """

        """
            hospital_id = response.xpath(
                '//h1/strong/a/@href').extract_first().split('/')[-1]
            logging.info('hospital_id--------------> : %s ' % hospital_id)
            hospital_comment_url = self.comment_template_url.format(hospital_id)
            #  hospital_comment_url = response.url.split('pageNo')[0]
            next_url = hospital_comment_url + \
                '?pageNo={}&sign={}&timestamp={}'.format(
                    next_page_no, sign, timestamp)

            logging.info('next_url--------------> : %s ' % next_url)
            #  self.driver.get(next_url)
            time.sleep(0.3)
            yield scrapy.Request(next_url, callback=self.parse_comment)
            """

        """
            if next_page_no < 5:
                for i in range(next_page_no, 5):
                    next_url = hospital_comment_url + \
                        '?pageNo={}&sign={}&timestamp={}'.format(
                            i, sign, timestamp)

                    logging.info(
                        'next_url--------------> : %s ' % next_url)
                    self.driver.get(next_url)
                    time.sleep(0.8)
                    yield scrapy.Request(next_url, callback=self.parse_comment)
            else:
                next_url = hospital_comment_url + \
                    '?pageNo={}&sign={}&timestamp={}'.format(
                        next_page_no, sign, timestamp)

                logging.info(
                    'next_url--------------> : %s ' % next_url)
                self.driver.get(next_url)
                time.sleep(0.8)
                yield scrapy.Request(next_url, callback=self.parse_comment)
            """

        #  if next_page_no <= 3500:
        #  yield scrapy.Request(next_url, cookies=self.driver.get_cookies(), callback=self.parse_comment)

        #  except Exception as e:
        #  logging.info('e: {}'.format(e))

        """
        # has next page
        #  self.driver.get(response.url)
        #  time.sleep(1)
        while True:
            try:
                #  next_page = self.driver.find_element_by_xpath(
                    #  '//div[@class="g-pagination"]/div/form/div[@class="pagers"]/a[contains(@class, "next")]')

                next_page = response.xpath(
                    '//div[@class="g-pagination"]/div/form/div[@class="pagers"]/a[contains(@class, "next")]')

                if next_page is None:
                    break

                # sign
                sign = response.xpath('//form[@class="qPagerForm"]/input[@name="sign"]/@value').extract_first()
                logging.info('sign--------------> : %s ' % sign)

                # timestamp
                timestamp = response.xpath('//form[@class="qPagerForm"]/input[@name="timestamp"]/@value').extract_first()
                logging.info('timestamp--------------> : %s ' % timestamp)

                #  'https://www.guahao.com/commentslist/h-af25fd28-0a0c-415a-b00a-24f1d4405b3c000/1-0?pageNo=2&sign=A069467567A3E903F777152708F9C5EEA864BE3A5888BD44E5BA169A01FB77B59C8A6ED97998CEE90DBC558C0A06B9EC2D2AFA4C1C965140D2BC2EE52C8AF64B&timestamp=1550646591738'
                next_url = response.url + 'pageNo={}sign={}&timestamp={}'.format(page_no, sign, timestamp)
                logging.info('next_url--------------> : %s ' % next_url)
                yield scrapy.Request(next_url, cookies=self.driver.get_cookies(), callback=self.parse_comment)

                page_no += 1

                #  next_page.click()
                #  # get the data and write it to scrapy items
                #  next_url = self.driver.current_url
                #  logging.info('--------------------> current_url: %s' % next_url)
                #  yield scrapy.Request(next_url, cookies=self.driver.get_cookies(), callback=self.parse_comment)
                #  yield SeleniumRequest(next_page, self.parse_comment)
            except:
                break
    """

    """
    def start_crawl(self, response):
        #  logging.info('cookie: {}'.format(self.driver.get_cookies()))
        logging.info('start_crawl.............')
        for page_num in range(self.min_page, self.max_page):
            url = self.start_url.format(page_num)
            #  time.sleep(1)
            #  yield SeleniumRequest(url=url, callback=self.parse)
            yield scrapy.Request(url, cookies=self.driver.get_cookies(), callback=self.parse)
    """

    def __del__(self):
        self.driver.close()
        self.hospital_set = None
        pass
